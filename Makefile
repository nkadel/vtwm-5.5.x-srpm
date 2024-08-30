#
# Build mock and local RPM versions of tools for Samba
#

# Assure that sorting is case sensitive
LANG=C

#
MOCKS+=alma+epel-8-x86_64
MOCKS+=alma+epel-9-x86_64
#MOCKS+=alma+epel-10-x86_64
MOCKS+=fedora-40-x86_64

REPOBASEDIR:=$(PWD)/repo

SPEC := `ls *.spec | head -1`

all:: $(MOCKS)

.PHONY: getsrc
getsrc::
	spectool -g $(SPEC)

srpm:: src.rpm

#.PHONY:: src.rpm
src.rpm:: Makefile
	@rm -rf rpmbuild
	@rm -f $@
	@echo "Building SRPM with $(SPEC)"
	rpmbuild --define '_topdir $(PWD)/rpmbuild' \
		--define '_sourcedir $(PWD)' \
		-bs $(SPEC) --nodeps
	mv rpmbuild/SRPMS/*.src.rpm src.rpm

.PHONY: build
build:: src.rpm
	rpmbuild --define '_topdir $(PWD)/rpmbuild' \
		--rebuild $?

.PHONY: $(MOCKS)
$(MOCKS):: src.rpm
	@set -o pipefail; ls -d $@/*.rpm 2>/dev/null | grep -q -v src.rpm  && \
	    echo "    RPMs in $@, skipping" && exit 0 || \
	    rm -rf $@ && \
	    echo "    Building $? in $@" && \
	    mock -q -r /etc/mock/$@.cfg \
		--resultdir=$(PWD)/$@ $?

mock:: $(MOCKS)

install:: $(MOCKS)
	@for repo in $(MOCKS); do \
	    echo Installing $$repo; \
	    case $$repo in \
		*-8-x86_64) yumrelease=el/8; yumarch=x86_64; ;; \
		*-9-x86_64) yumrelease=el/9; yumarch=x86_64; ;; \
		*-10-x86_64) yumrelease=el/10; yumarch=x86_64; ;; \
		*-40-x86_64) yumrelease=fedora/40; yumarch=x86_64; ;; \
		*-f40-x86_64) yumrelease=fedora/40; yumarch=x86_64; ;; \
		*-rawhide-x86_64) yumrelease=fedora/rawhide; yumarch=x86_64; ;; \
		*) echo "Unrecognized release for $$repo, exiting" >&2; exit 1; ;; \
	    esac; \
	    rpmdir=$(REPOBASEDIR)/$$yumrelease/$$yumarch; \
	    srpmdir=$(REPOBASEDIR)/$$yumrelease/SRPMS; \
	    echo "    Pushing SRPMS to $$srpmdir"; \
	    rsync -a $$repo/*.src.rpm --no-owner --no-group $$repo/*.src.rpm $$srpmdir/. || exit 1; \
	    createrepo -q $$srpmdir/.; \
	    echo "    Pushing RPMS to $$rpmdir"; \
	    rsync -a $$repo/*.rpm --exclude=*.src.rpm --exclude=*debuginfo*.rpm --no-owner --no-group $$repo/*.rpm $$rpmdir/. || exit 1; \
	    createrepo -q $$rpmdir/.; \
	done

clean::
	rm -rf */
	rm -f *.out
	rm -f *.rpm

realclean distclean:: clean
