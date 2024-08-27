import json
import random

from db import driver


def persist_records(driver, records):
    query = """
    UNWIND $records AS record
    CREATE (n:Profile {
        id: record.id,
        name: record.name,
        img: record.img,
        first_name: record.first_name,
        last_name: record.last_name,
        phone: record.phone,
        address: record.address,
        city: record.city,
        state: record.state,
        zipcode: record.zipcode,
        available: record.available
    })
    """
    with driver.session() as session:
        session.run(query, records=records)



def generate_records(profiles_total, friends_total, driver):
    records = []
    for i in range(profiles_total):
        record = {
            "id": i + 1,
            "name": i + 1,
            "img": "https://images.pexels.com/photos/220453/pexels-photo-220453.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500",
            "first_name": "FirstName_" + str(i + 1),
            "last_name": "LastName_" + str(i + 1),
            "phone": "(800) 555-{:04d}".format(i + 1),
            "address": str(i + 1) + " Some Street",
            "city": "City_" + str(i + 1),
            "state": "State_" + str(i + 1),
            "zipcode": "{:05d}".format(10000 + i),
            "available": True,
        }
        records.append(record)

    persist_records(driver, records)

    # Adding random friends
    relationships = set()
    with driver.session() as session:
        while len(relationships) < friends_total:
            person1, person2 = random.sample(range(1, profiles_total), 2)
            if (person1, person2) not in relationships and (person2, person1) not in relationships:
                relationships.add((person1, person2))
                session.run("""
                    MATCH
                    (p1:Profile {id: $id1}), (p2:Profile {id: $id2})
                    CREATE (p1)-[:FRIEND]->(p2),
                    (p2)-[:FRIEND]->(p1);
                    """, id1=person1, id2=person2
                )

    return records, relationships


if __name__ == "__main__":
    profiles_total = int(input("Enter the total number of Profiles to create: "))
    friends_total = int(input("Enter the total number of friends connections to create: "))

    profiles, relationships = generate_records(profiles_total, friends_total, driver)

    print(f"Generated profiles: \n {json.dumps(profiles, indent=4)}")

    print(f"Generated relationships: \n {relationships}")

