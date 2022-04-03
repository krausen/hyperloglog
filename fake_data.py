from faker import Faker
from faker.providers import internet
import redis


HYPERLOGLOG_KEY="krausen.github.io:unique_visits_hyperloglog"
SET_KEY="krausen.github.io:unique_visits_set"
DESIRED_CARDINALITY=10**7

r = redis.Redis(host='localhost', port=6379, db=0)


def _generate_fake_ips(n):
    """
    Try to generate a list n of public ips, cardinality and uniqueness is not guaranteed 
    """
    fake = Faker()
    fake.add_provider(internet)

    unique_ips = []
    for _ in range(n):
        unique_ips.append(fake.ipv4_public())
    return unique_ips


fake_ips=_generate_fake_ips(DESIRED_CARDINALITY)

for ip in fake_ips:
   r.pfadd(HYPERLOGLOG_KEY, ip)  # Add ip address to hyperloglog
for ip in fake_ips:
   r.sadd(SET_KEY, ip)  # Add ip to a regular set

hyper_loglog_count = r.pfcount(HYPERLOGLOG_KEY)  # Get cardinality from hyperloglog
set_count = r.scard(SET_KEY) # Get cardinality from set
hyper_loglog_mem_usage = r.memory_usage(HYPERLOGLOG_KEY) / 1024 # Get memory usage from hyperloglog
set_mem_usage = r.memory_usage(SET_KEY) / 1024  # Get memory usage from set
cardinality = len(set(fake_ips))  # Compute actual cardinality for reference
assert cardinality == set_count

print(f"set - count: {set_count}, mem_usage: {set_mem_usage}KiB")
print(f"hyper_loglog - count: {hyper_loglog_count}, mem_usage: {hyper_loglog_mem_usage}KiB")
print("error: " + str(round(((cardinality - hyper_loglog_count) / cardinality) * 100, 2)) + "%")
