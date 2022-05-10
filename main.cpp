#include <iostream>

#include "External/Dolphin-memory-engine/Source/DolphinProcess/DolphinAccessor.h"

int main() {
	std::cout << "Test" << std::endl;
	DolphinComm::DolphinAccessor t;
	t.init();
}
