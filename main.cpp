#include <iostream>
#include <cstring>
#include <optional>

#include "External/Dolphin-memory-engine/Source/DolphinProcess/DolphinAccessor.h"
#include "External/Dolphin-memory-engine/Source/Common/CommonUtils.h"

int main() {
	DolphinComm::DolphinAccessor::init();
	DolphinComm::DolphinAccessor::hook();

	if(DolphinComm::DolphinAccessor::getStatus() != DolphinComm::DolphinAccessor::DolphinStatus::hooked) {
		std::cout << "Did not hook properly" << std::endl;
	}

	std::cout << "Hooked to emulator successfully!" << std::endl;

	auto read_from_ram = [](const uint32_t offset, const size_t size, const Common::MemType type, const Common::MemBase base) -> std::optional<std::string> {
		char* buf = new char[size];
		if(DolphinComm::DolphinAccessor::readFromRAM(Common::dolphinAddrToOffset(offset, DolphinComm::DolphinAccessor::isARAMAccessible()), buf, getSizeForType(type, size), shouldBeBSwappedForType(type))) {
			std::cout << "Read successfully" << std::endl;
			std::string ret_val = Common::formatMemoryToString(buf, type, size, base, false);
			delete [] buf;
			return ret_val;
		}

		return std::nullopt;
	};

	auto result = read_from_ram(0x803C4C08, 2, Common::MemType::type_halfword, Common::MemBase::base_decimal);

	if(result.has_value()) {
		std::cout << *result << std::endl;
	} else {
		std::cout << "No result" << std::endl;
	}
}
