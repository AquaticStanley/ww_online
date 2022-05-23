#include "dme_bindings.h"

#include "External/Dolphin-memory-engine/Source/DolphinProcess/DolphinAccessor.h"
#include "External/Dolphin-memory-engine/Source/Common/CommonUtils.h"

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

	py::enum_<Common::MemType>(m, "MemType")
		.value("BYTE", Common::MemType::type_byte)
		.value("HALFWORD", Common::MemType::type_halfword)
		.value("WORD", Common::MemType::type_word)
		.value("FLOAT", Common::MemType::type_float)
		.value("DOUBLE", Common::MemType::type_double)
		.value("STRING", Common::MemType::type_string)
		.value("BYTEARRAY", Common::MemType::type_byteArray)
		.value("NUM", Common::MemType::type_num)
		.export_values()
	;

	py::enum_<Common::MemBase>(m, "MemBase")
		.value("DEC", Common::MemBase::base_decimal)
		.value("HEX", Common::MemBase::base_hexadecimal)
		.value("OCT", Common::MemBase::base_octal)
		.value("BIN", Common::MemBase::base_binary)
		.value("NONE", Common::MemBase::base_none)
		.export_values()
	;

	py::class_<DolphinAccessor>(m, "DolphinAccessor")
		.def(py::init<>())
		.def_static("init", &DolphinAccessor::init)
		.def_static("hook", &DolphinAccessor::hook)
		.def_static("unhook", &DolphinAccessor::unHook)
		.def_static("read_from_ram", [](const uint32_t offset, const size_t size, const Common::MemType type, const Common::MemBase base) -> std::optional<std::string> {
			char* buffer = new char[size];
			if(DolphinComm::DolphinAccessor::readFromRAM(Common::dolphinAddrToOffset(offset, DolphinComm::DolphinAccessor::isARAMAccessible()), buffer, getSizeForType(type, size), shouldBeBSwappedForType(type))) {
				std::string ret_val = Common::formatMemoryToString(buffer, type, size, base, false);
				delete [] buffer;
				return ret_val;
			}

			return std::nullopt;
		})
		.def_static("write_to_ram", [](const uint32_t offset, uint64_t value, const size_t size, const Common::MemType type) {
			char* buffer = new char[size];
			std::memcpy(buffer, &value, sizeof(value));
			DolphinComm::DolphinAccessor::writeToRAM(Common::dolphinAddrToOffset(offset, DolphinComm::DolphinAccessor::isARAMAccessible()), buffer, getSizeForType(type, size), shouldBeBSwappedForType(type));
			delete [] buffer;
		})
		.def_static("write_to_ram", [](const uint32_t offset, float value, const size_t size, const Common::MemType type) {
			char* buffer = new char[size];
			std::memcpy(buffer, &value, sizeof(value));
			DolphinComm::DolphinAccessor::writeToRAM(Common::dolphinAddrToOffset(offset, DolphinComm::DolphinAccessor::isARAMAccessible()), buffer, getSizeForType(type, size), shouldBeBSwappedForType(type));
			delete [] buffer;
		})
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
