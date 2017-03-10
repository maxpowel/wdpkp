from fastkml import kml
import database
import re
from model import Device, DeviceLocation, DeviceType, Manufacturer, EncryptionType
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime
import sys
import os.path

def main(filename):
    session = database.Session()
    cache = database.CachedFinder(session)
    k = kml.KML()

    with open(filename, 'rb') as f:
        k.from_string(f.read())

    document = list(k.features())[0]
    folders = document.features()
    print("Processing {filename}...".format(filename=filename))
    count = 0
    for folder in folders:
        if folder.name == "Routes":
            # Simply ignore the routes information
            continue

        for place in folder.features():
            # Only process entries that have a description
            if place.description is not None:
                # Counter for debug reasons
                count += 1
                if count % 50 == 0:
                    print(count)

                # Build a dictionary with the content of the description of the placemark
                attributes = {c[0].strip(): c[1].strip() for c in [c.split(":", 1) for c in place.description.replace("<br />", "").split("\n") if len(c) > 0]}
                # No mac means useless entry, we ignore it
                if "MAC" in attributes:
                    date = datetime.strptime(attributes['Last time'], '%a %b %d %X %Y')
                    # Remove trash from encryption types (html tags)
                    attributes['Encryption'] = re.sub(r'<FONT color=[a-z]+>', '', attributes['Encryption'].replace('</FONT>', '')).split(" ")

                    # Lookup for existing device or create new
                    try:
                        device = session.query(Device).filter(Device.mac == attributes["MAC"]).one()
                    except NoResultFound:
                        device = Device()
                        device.mac = attributes["MAC"]
                        device.created_at = date
                        session.add(device)

                    # Populate the rest of properties
                    device.ssid = attributes["SSID"]
                    device.channel = attributes["Channel"]
                    device.type = cache.get(DeviceType, attributes["Type"])
                    device.manufacturer = cache.get(Manufacturer, attributes["Manuf"])

                    # coordenadas: latitude, longitud, cogerlas de la descripción. En el tag <coordinates> están al revés
                    coordinates = attributes["GPS"].split(",")
                    device.locations.append(DeviceLocation(latitude=coordinates[0], longitude=[coordinates[1]]))

                    for encryption in attributes['Encryption']:
                        device.encryptions.append(cache.get(EncryptionType, encryption))

                    device.updated_at = date

    session.commit()
    session.close()
    print("Successfully processed {total} entries".format(total=count))

if __name__ == "__main__":

    if len(sys.argv) is not 2:
        print("usage: python {script} filename.kml".format(script=sys.argv[0]))
    elif not os.path.isfile(sys.argv[1]):
        print("Error: File {filename} does not exists".format(filename=sys.argv[1]))
    else:
        main(sys.argv[1])
