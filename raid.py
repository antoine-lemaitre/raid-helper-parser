import json
import itertools



class Raid:

    def __init__(self, event_name, date, time, description, created_by, link):
        self.event_name = event_name
        self.date = date
        self.time = time
        self.description = description
        self.created_by = created_by
        self.link = link
        self.tank = []
        self.hunter = []
        self.priest = []
        self.warrior = []
        self.mage = []
        self.paladin = []
        self.rogue = []
        self.warlock = []
        self.druid = []
        self.late = []
        self.bench = []
        self.absence = []

    def add_attendee(self, role, name):
        role = role.lower()
        if role == "tank":
            self.tank.append(name)
        elif role == "hunter":
            self.hunter.append(name)
        elif role == "priest":
            self.priest.append(name)
        elif role == "warrior":
            self.warrior.append(name)
        elif role == "mage":
            self.mage.append(name)
        elif role == "paladin":
            self.paladin.append(name)
        elif role == "rogue":
            self.rogue.append(name)
        elif role == "warlock":
            self.warlock.append(name)
        elif role == "druid":
            self.druid.append(name)
        elif role == "late":
            self.late.append(name)
        elif role == "bench":
            self.bench.append(name)
        elif role == "absence":
            self.absence.append(name)
                    
    def get_event_name(self):
        return self.event_name

    def get_date(self):
        return self.date

    def get_tanks(self):
        return self.tank

    def get_hunters(self):
        return self.hunter

    def get_priests(self):
        return self.priest

    def get_warriors(self):
        return self.warrior

    def get_mages(self):
        return self.mage

    def get_paladins(self):
        return self.paladin

    def get_rogues(self):
        return self.rogue

    def get_warlocks(self):
        return self.warlock

    def get_druids(self):
        return self.druid

    def get_late(self):
        return self.late

    def get_bench(self):
        return self.bench

    def get_absence(self):
        return self.absence

    def get_attendees(self):
        attendees = list(itertools.chain(self.tank, self.hunter, self.priest, self.warrior, self.mage, self.paladin, self.rogue, self.warlock, self.druid))
        return attendees


    def export_attendence_to_json(self):
        json_export = {
            "event_name": self.get_event_name(),
            "date": self.get_date(),
            "attendees": self.get_attendees(),
        }
        return json_export

