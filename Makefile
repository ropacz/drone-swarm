all: checkmakefiles
	cd src && $(MAKE)

clean: checkmakefiles
	cd src && $(MAKE) clean

cleanall: checkmakefiles
	cd src && $(MAKE) MODE=release clean
	cd src && $(MAKE) MODE=debug clean
	rm -f src/Makefile

makefiles:
	cd src && opp_makemake -f --deep -O ../out -KINET_PROJ=/Users/rodrigo/omnetpp-workspace/inet-4.5.4 -DINET_IMPORT -I/Users/rodrigo/omnetpp-workspace/inet-4.5.4/src -L/Users/rodrigo/omnetpp-workspace/inet-4.5.4/src -lINET

checkmakefiles:
	@if [ ! -f src/Makefile ]; then \
	echo; \
	echo '======================================================================='; \
	echo 'src/Makefile does not exist. Please use "make makefiles" to generate it!'; \
	echo '======================================================================='; \
	echo; \
	exit 1; \
	fi
