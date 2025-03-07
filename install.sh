mkdir External
mkdir External/Dolphin-memory-engine
mkdir External/pybind
mkdir External/pybind/pybind11
git clone https://github.com/aldelaro5/Dolphin-memory-engine.git External/Dolphin-memory-engine
git clone https://github.com/pybind/pybind11.git External/pybind/pybind11
cd External/Dolphin-memory-engine && git checkout dad2875d9a52c06826825b685c1eddccccf50796 && cd -;
