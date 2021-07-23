from api import models
from django.core.management.base import BaseCommand

import csv
import dateutil.parser


def export_file():
    file_name = "dpu_data.csv"
    models.Space.objects.all().delete()
    models.Doorway.objects.all().delete()
    models.DPU.objects.all().delete()
    models.Events.objects.all().delete()
    models.RealtimeSpaceData.objects.all().delete()

    spaces = models.Space.objects.bulk_create([models.Space(name=x) for x in "ABCDFE"])
    doors = models.Doorway.objects.bulk_create(
        [
            models.Doorway(name=x, egress_spc=spaces[1], ingress_spc=spaces[2])
            for x in reversed("ZXCVW")
        ]
    )

    dpu_mapping = {
        "423": models.DPU.objects.get_or_create(name="423", door=doors[1]),
        "283": models.DPU.objects.get_or_create(name="283", door=doors[0]),
    }
    records = []
    with open(file_name, newline="") as csvfile:
        for r in list(csv.reader(csvfile))[1:]:
            dt, direction, dpu = r
            direction = int(direction)
            records.append(
                dict(
                    created_at=dateutil.parser.isoparse(dt),
                    direction=direction,
                    id=dpu,
                )
            )
            dpu, _ = dpu_mapping.get(dpu)
            inn, out = models.DPU.objects.motion_direction(dpu, direction)

            rev, _ = models.RealtimeSpaceData.objects.get_or_create(space=inn)
            rev.count += 1
            rev.save()
            _ = models.Events.objects.create(
                door=dpu.door, space=inn, direction=direction, new_count=rev.count
            )

            rev, _ = models.RealtimeSpaceData.objects.get_or_create(space=out)
            rev.count -= 1
            rev.save()

            _ = models.Events.objects.create(
                door=dpu.door, space=out, direction=direction, new_count=rev.count
            )


class Command(BaseCommand):
    help = "Load dpu from a csv file"

    def handle(self, *args, **kwargs):
        export_file()
        self.stdout.write("Done")
