import dme

def read_from_ram(json_entry):
	return dme.DolphinAccessor.read_from_ram(int(json_entry['location'], 16),
											 json_entry['size'],
											 dme.MemType.__members__[json_entry['mem_type']],
											 dme.MemBase.__members__[json_entry['mem_base']])

def write_to_ram(json_entry, value):
	return dme.DolphinAccessor.write_to_ram(int(json_entry['location'], 16),
											value,
											json_entry['size'],
											dme.MemType.__members__[json_entry['mem_type']])
