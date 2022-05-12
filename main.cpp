#include <iostream>
#include <cstring>

#include "External/Dolphin-memory-engine/Source/DolphinProcess/DolphinAccessor.h"
#include "External/Dolphin-memory-engine/Source/Common/CommonUtils.h"

int main() {
	DolphinComm::DolphinAccessor::init();
	DolphinComm::DolphinAccessor::hook();

	if(DolphinComm::DolphinAccessor::getStatus() != DolphinComm::DolphinAccessor::DolphinStatus::hooked) {
		std::cout << "Did not hook properly" << std::endl;
	}

	std::cout << "Hooked to emulator successfully!" << std::endl;

	size_t m_length = 2;
	Common::MemType m_type = Common::MemType::type_halfword;
	Common::MemBase m_base = Common::MemBase::base_decimal;
	bool m_isUnsigned = false;
	char* m_memory = new char[m_length];
	if (DolphinComm::DolphinAccessor::readFromRAM(Common::dolphinAddrToOffset(0x803C4C08, DolphinComm::DolphinAccessor::isARAMAccessible()), m_memory, getSizeForType(m_type, m_length), shouldBeBSwappedForType(m_type))) {
		std::cout << "Read successfully" << std::endl;

		std::string s = Common::formatMemoryToString(m_memory, m_type, m_length, m_base, m_isUnsigned);
		std::cout << s << std::endl;
	}
}
