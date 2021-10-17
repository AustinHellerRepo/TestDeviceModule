from austin_heller_repo.socket import start_thread, time, json
from austin_heller_repo.module import Module, ModuleMessage


class ImplementedModule(Module):

	def __init__(self, *, device_guid: str, device_instance_guid: str, send_message_method, get_devices_by_purpose_method):
		super().__init__(
			device_guid=device_guid,
			device_instance_guid=device_instance_guid,
			send_message_method=send_message_method,
			get_devices_by_purpose_method=get_devices_by_purpose_method
		)

		print("__init__")

		self.__is_module_thread_running = False
		self.__module_thread = None

	def receive(self, *, module_message: ModuleMessage):

		_json_string = json.dumps(module_message.get_transmission_json())
		print("received: \"" + _json_string + "\"")

	def start(self):

		self.__is_module_thread_running = True
		self.__module_thread = start_thread(self.__thread_method)

	def stop(self):

		self.__is_module_thread_running = False
		self.__module_thread.join()

	def get_purpose_guid(self) -> str:
		return "091CEE3D-D683-4B31-ABCE-A0AC568FF14B"

	def __thread_method(self):

		_queue_guid = "D5195218-61F6-4EDF-8675-ABB279BA92CD"

		self._send(
			module_message=ModuleMessage(
				queue_guid=_queue_guid,
				transmission_json={
					"message": "started"
				},
				source_device_guid=self._get_device_guid(),
				source_device_instance_guid=self._get_device_instance_guid(),
				destination_device_guid=self._get_device_guid(),
				destination_device_instance_guid=self._get_device_instance_guid()
			)
		)

		_iteration = 0
		while self.__is_module_thread_running:
			time.sleep(1.0)
			_message = str(_iteration)
			print("sending: \"" + _message + "\"")

			self._send(
				module_message=ModuleMessage(
					queue_guid=_queue_guid,
					transmission_json={
						"message": _message
					},
					source_device_guid=self._get_device_guid(),
					source_device_instance_guid=self._get_device_instance_guid(),
					destination_device_guid=self._get_device_guid(),
					destination_device_instance_guid=self._get_device_instance_guid()
				)
			)

			_iteration += 1

		self._send(
			module_message=ModuleMessage(
				queue_guid=_queue_guid,
				transmission_json={
					"message": "ended"
				},
				source_device_guid=self._get_device_guid(),
				source_device_instance_guid=self._get_device_instance_guid(),
				destination_device_guid=self._get_device_guid(),
				destination_device_instance_guid=self._get_device_instance_guid()
			)
		)
