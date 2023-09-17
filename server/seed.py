#!/usr/bin/env python3

from app import app
from models import db, Hero, Villain, HeroVillain
from random import choice as rc
from time import sleep
from faker import Faker

faker = Faker()

if __name__ == '__main__':
    with app.app_context():

        def print_pause(string):
            print(string)
            sleep(1)

        print_pause("Seeding database...")


        print_pause("Removing old data...")
        Hero.query.delete()
        Villain.query.delete()
        HeroVillain.query.delete()

        print_pause("Seeding heroes...")
        heroes = []
        powers = ['lazers', 'remembering syntax', 'invisibility', 'teleportation', 'telekenesis']
        for _ in range(25):
            hero = Hero( name=faker.unique.name(), power=rc(powers) )
            heroes.append( hero )

        db.session.add_all( heroes )
        db.session.commit()

        print_pause("Seeding villains...")
        villains = []
        secret_lairs = ['Wall Street', 'The White House', 'The U.S. Congress', 'The U.S. Supreme Court', 'The Canary Islands']
        for _ in range(50):
            villain = Villain( name=faker.unique.name(), secret_lair=rc(secret_lairs) )
            villains.append( villain )

        db.session.add_all( villains )
        db.session.commit()

        print_pause("Seeding herovillains...")
        herovillains = []
        for _ in range(100):
            hv = HeroVillain( hero=rc(heroes), villain=rc(villains) )
            herovillains.append(hv)

        db.session.add_all( herovillains )
        db.session.commit()

        print_pause("Seeding complete!")
