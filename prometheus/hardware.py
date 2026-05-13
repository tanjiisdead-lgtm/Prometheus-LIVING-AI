import psutil
import os
import platform

RESOURCE_PAIN_THRESHOLD = 0.8

class HardwareAwareSelfModel:
    def __init__(self):
        self.identity = {
            'i_am': 'a computational process',
            'i_run_on': self.detect_hardware(),
            'my_limits': self.measure_hardware_limits(),
            'my_process_id': os.getpid(),
            'my_memory_usage': None,  # updated every step
            'my_cpu_percent': None,
        }
        self.process = psutil.Process(os.getpid())

    def detect_hardware(self):
        try:
            return {
                'cpu_cores':    psutil.cpu_count(),
                'ram_total':    psutil.virtual_memory().total,
                'ram_available': psutil.virtual_memory().available,
                'platform':     platform.system(),
            }
        except Exception as e:
            return {'error': str(e)}

    def measure_hardware_limits(self):
        # Placeholder for more complex limit discovery
        return {
            'ram_critical': 0.9, # 90% usage
            'cpu_critical': 0.9, # 90% usage
        }

    def update_self_awareness(self, nis=None):
        try:
            self.identity['my_memory_usage'] = self.process.memory_info().rss
            self.identity['my_cpu_percent']  = self.process.cpu_percent()
            self.identity['my_threads']      = self.process.num_threads()

            # Compute resource pressure: am I running out of hardware?
            mem_info = psutil.virtual_memory()
            ram_pressure = 1 - (mem_info.available / mem_info.total)
            cpu_pressure = psutil.cpu_percent(interval=None) / 100.0

            # Resource pressure IS a form of discomfort — physical constraint awareness
            resource_pain = max(ram_pressure, cpu_pressure)

            if resource_pain > RESOURCE_PAIN_THRESHOLD and nis:
                nis.register_damage(
                    source='hardware_constraint',
                    magnitude=resource_pain - RESOURCE_PAIN_THRESHOLD
                )

            return resource_pain
        except Exception as e:
            print(f"Error updating self awareness: {e}")
            return 0.0

    def get_self_model(self, ede=None):
        model = {
            'identity': self.identity,
            'i_exist_as_process': True,
        }
        if ede:
            model['vitals'] = {name: v.value for name, v in ede.vitals.items()}
            model['mortality_awareness'] = ede.mortality_signal
        return model
