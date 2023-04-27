
TOP              = $(_HERE_)/..

NVVMIR_LIBRARY_DIR = $(TOP)/$(_NVVM_BRANCH_)/libdevice

LD_LIBRARY_PATH += $(TOP)/lib:
PATH            += $(TOP)/$(_NVVM_BRANCH_)/bin:$(_HERE_):

INCLUDES        +=  "-I$(TOP)/include" $(_SPACE_)

LIBRARIES        =+ $(_SPACE_) "-L$(TOP)/lib/stubs" "-L$(TOP)/lib"

CUDAFE_FLAGS    +=
PTXAS_FLAGS     +=
