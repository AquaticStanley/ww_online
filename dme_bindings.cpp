#include "dme_bindings.h"

#include <iostream>

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
		.def_static("read_from_ram", [](const uint32_t offset, const size_t size, const bool withBSwap) {
			// char* buf = new char[size];
			// bool read = DolphinAccessor::readFromRAM(offset, buf, size, withBSwap);
			// if(DolphinComm::DolphinAccessor::readFromRAM(Common::dolphinAddrToOffset(0x803C4C08, DolphinComm::DolphinAccessor::isARAMAccessible()), m_memory, sizeof(m_length), shouldBeBSwappedForType(m_type))) {
				
			// }
			// if(!read) {
			// 	std::cout << "Did not read correctly" << std::endl;
			// }
			// std::string ret_val = Common::formatMemoryToString(buf, Common::MemType::type_halfword, size, Common::MemBase::base_hexadecimal, true, withBSwap);
			// std::cout << ret_val << std::endl;
			// delete [] buf;
			// return ret_val;
			// uint16_t ret_val;
			// std::memcpy(&ret_val, buf, size);
			// return ret_val;
		})
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

	m.def("dolphin_addr_to_offset", &Common::dolphinAddrToOffset);
	m.def("offset_to_dolphin_addr", &Common::offsetToDolphinAddr);
	m.def("format_memory_to_str", &Common::formatMemoryToString);
}
