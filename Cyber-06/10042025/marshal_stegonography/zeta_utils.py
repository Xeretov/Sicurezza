import marshal

# Example of valid marshaled data
data = compile("print('flag{marshal_exec_payload}')", "<string>", "exec")
valid_data = marshal.dumps(data)

# unmarshal the data
def unmarshal(data):
    try:
        return marshal.loads(data)
    except Exception as e:
        print(f"Error: {e}")
        return None

print(marshal.dumps(unmarshal(valid_data)))  # Should print: flag{marshal_exec_payload}

