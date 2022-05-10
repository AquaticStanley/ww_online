#include "dme_bindings.h"

PYBIND11_MODULE(dme, m) {
	using namespace DolphinComm;

	py::enum_<DolphinAccessor::DolphinStatus>(m, "DolphinStatus")
		.value("hooked", DolphinAccessor::DolphinStatus::hooked)
		.value("not_running", DolphinAccessor::DolphinStatus::notRunning)
		.value("no_emulator", DolphinAccessor::DolphinStatus::noEmu)
		.value("unhooked", DolphinAccessor::DolphinStatus::unHooked)
		.export_values()
	;

	py::class_<DolphinAccessor>(m, "DolphinAccessor")
		.def_static("init", &DolphinAccessor::init)
		// .def("hook", &DolphinAccessor::hook)
		// .def("unhook", &DolphinAccessor::unHook)
		// .def("read_from_ram", &DolphinAccessor::readFromRAM)
		// .def("write_to_ram", &DolphinAccessor::writeToRAM)
		// .def("get_pid", &DolphinAccessor::getPID)
		// .def("get_emu_ram_addr_start", &DolphinAccessor::getEmuRAMAddressStart)
		// .def("get_status", &DolphinAccessor::getStatus)
		// .def("is_aram_accessible", &DolphinAccessor::isARAMAccessible)
		// .def("get_aram_addr_start", &DolphinAccessor::getARAMAddressStart)
		// .def("is_mem2_present", &DolphinAccessor::isMEM2Present)
		// .def("get_ram_cache", &DolphinAccessor::getRAMCache)
		// .def("get_ram_cache_size", &DolphinAccessor::getRAMCacheSize)
		// .def("update_ram_cache", &DolphinAccessor::updateRAMCache)
		// .def("get_formatted_value_from_cache", &DolphinAccessor::getFormattedValueFromCache)
		// .def("copy_raw_memory_from_cache", &DolphinAccessor::copyRawMemoryFromCache)
		// .def("is_valid_console_addr", &DolphinAccessor::isValidConsoleAddress)
	;
}
