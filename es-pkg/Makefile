sources:
	export OLD_PATH=$$(pwd);\
	cd ..;  \
		export NAME=$$(python setup.py --name);\
		export PBR_VERSION=$$(python -c "from pbr.version import VersionInfo;\
		print VersionInfo(\"$${NAME}\").semantic_version().decrement().\
				brief_string()");\
		python setup.py sdist -d es-pkg/
	cd $${OLD_PATH}
