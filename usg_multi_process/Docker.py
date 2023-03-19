from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient

# 2023-03-20 Useop Gim(c) GNU3.0 Affero
# Verison 1.0 
  
def docker_install_ec2(self, 
                         host_name:str, 
                         user_name:str, 
                         key_filename:str, 
                         docker_image_file:str):
    """
    Installing docker using the cloud service in linux os
    """

      ssh = SSHClient()
      ssh.set_missing_host_key_policy(AutoAddPolicy())

      # connection
      ssh.connect(hostname=host_name, username=user_name, key_filename=key_filename)

      # Docker install
      stdin, stdout, stderr = ssh.exec_command('sudo yum install docker -y')
      print(stdout.read().decode())

      # Docker start
      stdin, stdout, stderr = ssh.exec_command('sudo service docker start')
      print(stdout.read().decode())

      # send docekr tar file
      with SCPClient(ssh.get_transport()) as scp:
          scp.put(f'{docker_image_file}.tar')

      # load docker tar file for install image
      stdin, stdout, stderr = ssh.exec_command(f'sudo docker load -i {docker_image_file}.tar')
      print(stdout.read().decode())

      # Docker image list check
      stdin, stdout, stderr = ssh.exec_command('sudo docker images')
      print(stdout.read().decode())

      # Docker image build
      stdin, stdout, stderr = ssh.exec_command(f'sudo docker build -t {docker_image_file} .')
      print(stdout.read().decode())

      # SSH close
      ssh.close()

def access_cloud_service(self, 
                    host_name:str, 
                    user_name:str, 
                    key_filename:str,
                    docker_image_file:str):
    """
    Actual run docker file on the cloud service
    """
    
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(AutoAddPolicy())

    ssh.connect(hostname=host_name, username=user_name, key_filename=key_filename)

    # run docker image if window exe file else run docker image
    stdin, stdout, stderr = ssh.exec_command(
        f'sudo docker run -name {docker_image_file}')
    print(stdout.read().decode())

    # SSH close
    ssh.close()
