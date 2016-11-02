#!/local/bin/python
import luigi
from docker import Client
from time import sleep

class  LongTask(luigi.Task):

    def output(self):
        return luigi.LocalTarget("db.txt")

    def run(self):
        dock = Client(base_url='unix://var/run/docker.sock')
        host_config = dock.create_host_config(publish_all_ports=True)
        c1 = dock.create_container(image='redis:latest', ports=[6379], name='db', host_config=host_config)
        c1_run = dock.start(container=c1.get('Id'))
        sleep(30)
        with self.output().open("w") as out_file:
            out_file.write("up")

class WriteTask(luigi.Task):

    def output(self):
        return luigi.LocalTarget("write.txt")

    def run(self):
        dock = Client(base_url='unix://var/run/docker.sock')
        db_info = dock.inspect_container('db')
        db_ip = db_info['NetworkSettings']['Networks']['bridge']['IPAddress']
        c2 = dock.create_container(image='writer', name='writer', environment=["DB_IP=" + db_ip])
        c2_run = dock.start(container=c2.get('Id'))
        with self.output().open("w") as out_file:
            out_file.write('written')

    def requires(self):
        return LongTask()

class ReadTask(luigi.Task):

    def output(self):
        return luigi.LocalTarget("read.txt")

    def run(self):
        dock = Client(base_url='unix://var/run/docker.sock')
        db_info = dock.inspect_container('db')
        db_ip = db_info['NetworkSettings']['Networks']['bridge']['IPAddress']
        host_config = dock.create_host_config(binds=['/var/tmp/share:/share'])
        c3 = dock.create_container(image='reader', detach=True, volumes=['/share'], name='reader', host_config=host_config, environment=["DB_IP=" + db_ip])
        c3_run = dock.start(container=c3.get('Id'))
        with self.output().open("w") as out_file:
            out_file.write('read')

    def requires(self):
        return WriteTask()

if __name__ == '__main__':
    global dock
    dock = Client(base_url='unix://var/run/docker.sock')
    luigi.run(["--local-scheduler"],ReadTask)
