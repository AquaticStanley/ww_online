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
		.def(py::init<>())
		.def_static("init", &DolphinAccessor::init)
		.def_static("hook", &DolphinAccessor::hook)
		.def_static("unhook", &DolphinAccessor::unHook)
		.def_static("read_from_ram", &DolphinAccessor::readFromRAM)
		.def_static("write_to_ram", &DolphinAccessor::writeToRAM)
		.def_static("get_pid", &DolphinAccessor::getPID)
		.def_static("get_emu_ram_addr_start", &DolphinAccessor::getEmuRAMAddressStart)
		.def_static("get_status", &DolphinAccessor::getStatus)
		.def_static("is_aram_accessible", &DolphinAccessor::isARAMAccessible)
		.def_static("get_aram_addr_start", &DolphinAccessor::getARAMAddressStart)
		.def_static("is_mem2_present", &DolphinAccessor::isMEM2Present)
		.def_static("get_ram_cache", &DolphinAccessor::getRAMCache)
		.def_static("get_ram_cache_size", &DolphinAccessor::getRAMCacheSize)
		.def_static("update_ram_cache", &DolphinAccessor::updateRAMCache)
		.def_static("get_formatted_value_from_cache", &DolphinAccessor::getFormattedValueFromCache)
		.def_static("copy_raw_memory_from_cache", &DolphinAccessor::copyRawMemoryFromCache)
		.def_static("is_valid_console_addr", &DolphinAccessor::isValidConsoleAddress)
	;
}
