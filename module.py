from austin_heller_repo.socket import Module, start_thread, time


class ImplementedModule(Module):

	def __init__(self):
		super().__init__()

		print("__init__")

		self.__is_module_thread_running = False
		self.__module_thread = None

	def receive(self, *, data: str):

		print("received: \"" + data + "\"")

	def start(self):

		self.__is_module_thread_running = True
		self.__module_thread = start_thread(self.__thread_method)

	def stop(self):

		self.__is_module_thread_running = False
		self.__module_thread.join()

	def get_purpose_guid(self) -> str:
		return "091CEE3D-D683-4B31-ABCE-A0AC568FF14B"

	def __thread_method(self):

		self.get_send_method()("started")
		_iteration = 0
		while self.__is_module_thread_running:
			time.sleep(1.0)
			_message = str(_iteration)
			print("sending: \"" + _message + "\"")
			self.get_send_method()(_message)
			_iteration += 1
		self.get_send_method()("ended")

