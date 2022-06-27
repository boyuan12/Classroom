from string import ascii_lowercase
import random
import cloudconvert


def random_str(digit=7):
    return "".join([random.choice(ascii_lowercase) for _ in range(digit)])

cloudconvert.configure(api_key="eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiY2UwNTk4NzRhMDM4ZDgwZTU0YzllMDNlZDNlZGVlMDA5MDkzMDhkZDkzNmU5N2E3Mjk2NzJiNDI1MGVlNzg4MzYxNTg1ZWQxY2U0NzI4MzMiLCJpYXQiOjE2NTU3MDQ5NDYuMDM0NzAzLCJuYmYiOjE2NTU3MDQ5NDYuMDM0NzA0LCJleHAiOjQ4MTEzNzg1NDYuMDI5NjQxLCJzdWIiOiI1ODU0MTUwNSIsInNjb3BlcyI6WyJ1c2VyLnJlYWQiLCJ1c2VyLndyaXRlIiwidGFzay5yZWFkIiwidGFzay53cml0ZSIsIndlYmhvb2sucmVhZCIsIndlYmhvb2sud3JpdGUiLCJwcmVzZXQucmVhZCIsInByZXNldC53cml0ZSJdfQ.AYPPbRwSj4yBuiTdhPuvRGPkmim9p09IvP_FbSrDVkvJbJg95EA2d_AhmnbmrfGPxJbXFn8bSSoVeSKctbC8iDVnYxDQWrZv5qd_ivS-pGPfZ078uOSG5-sgxYp_eY3TQ2PLxjeK1uqhjkNigTO4McG1mHpZgzfubWu52gei717CJ15eDUI5yHIN7OVJuUI3DS0zb_Cw4JjOvf3DVCt4t-2l9Pmx7VqZyOPQbbKxC33s6DlYwexb3augWHn3inffH8EgU-b4PUUDDDvruA7gDsl0kl3WSjcCJD69ffSuFmGKRFrHoKWd2uh8uTGOaWwIZkO-jiSJVQNDcEKmZaBERhxmGIkckaQ3wqdY4syS7XozA1m43PBLtZbsY-js-_ssOqsfQCE2FKAfaj6wOXR0zAO8oAvCxRJs6AT-FlPflEA7zxNa7PXiZvXUtwmdpmTSob8Td6x5QUGRBzfDI0T_LNyISpnOpRBEJNKnbsmpedmGt811iTn60rv34528It_3JdCNp4e3ITMVzo1PCYXHFLaCwLns-_C9KT0fEfWD3j8SaqGNZ7qm61GRjkarAxx7jHpcJjoys2Sfeu29QpVzo9u_ud-KEVjsVjVnpDl-FtFlcLkMzBY-EOAb0739Xh1BEfjdx8S-b5F1AzjbFG-zM2IKLn5LJwM2PuL3TDykm1w")

def convert_file(original_url, output_file_format):
    job = cloudconvert.Job.create(payload={
        "tasks": {
            'import-my-file': {
                'operation': 'import/url',
                'url': original_url
            },
            'convert-my-file': {
                'operation': 'convert',
                'input': 'import-my-file',
                'output_format': output_file_format,
            },
            'export-my-file': {
                'operation': 'export/url',
                'input': 'convert-my-file'
            }
        }
    })

    export_task_id = job["tasks"][2]["id"]

    res = cloudconvert.Task.wait(id=export_task_id) # Wait for job completion
    file = res.get("result").get("files")[0]
    return file["url"]