import click
import uuid
import sqlite3
import csv

from dataclasses import dataclass

db = sqlite3.connect("test.db")
cursor = db.cursor()

@dataclass
class Item:
    id: uuid.UUID
    name: str
    category : str
    price : float


@click.group()
def cli():
    pass

# Les differentes entrées
@cli.command()
@click.option("-n", "--name", prompt="Saisissez le nom ", help="The name of the item.")
@click.option("-c", "--category", prompt="Saisissez la catégorie ", help="The name of the category.")
@click.option("-p", "--price", prompt="Price", help="Saisissez le montant")
# Partie C du CRUD (create , read , update, delete)
def display(name: str , category: str , price: float):
    item = Item(uuid.uuid4(), name , category , price)
    

    click.echo("Nom : " + item.name + "Categorie : " + item.category + "Montant : " + item.price + "€ ")

    
    
     

# Les differentes entrées
@cli.command()
@click.option("-n", "--name", prompt="Saisissez le nom ", help="The name of the item.")
@click.option("-c", "--category", prompt="Saisissez la catégorie ", help="The name of the category.")
@click.option("-p", "--price", prompt="Price", help="Saisissez le montant")

def add_BD(name , category , price): 
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS budget (
        id TEXT PRIMARY KEY,
        name TEXT,
        category TEXT,
        price FLOAT
        )"""
    )
    

    db.commit()
    db.close()


# Les differentes entrées
@cli.command()
@click.option("-n", "--name", prompt="Saisissez le nom ", help="The name of the item.")
@click.option("-c", "--category", prompt="Saisissez la catégorie ", help="The name of the category.")
@click.option("-p", "--price", prompt="Price", help="Saisissez le montant")

def insertion (name , category , price):

    db.execute("""
        INSERT INTO budget (id, name, category, price)
        VALUES (?, ?, ?, ?)
        """, (str(uuid.uuid4()), name, category, price))

    db.commit()
    db.close()


@cli.command()
@click.argument("csv_file", type=click.Path(exists=True))
def import_csv(csv_file):
    db = sqlite3.connect("test.db") 
    cursor = db.cursor()

    with open(csv_file, newline='', encoding='utf-8') as f:  # Ouvrir le fichier
        reader = csv.reader(f, delimiter=',')
        next(reader)  # Sauter l'en-tête

        for row in reader:
            name, category, price = row
            cursor.execute(
                "INSERT INTO budget (id, name, category, price) VALUES (?, ?, ?, ?)",
                (str(uuid.uuid4()), name, category, float(price))  # Convertir price en float
            )

    db.commit()
    db.close()
    click.echo("Importation réussie !")

@cli.command()
@click.argument("csv_file", type=click.Path(writable=True, dir_okay=True))
def export_csv(csv_file):
    db = sqlite3.connect("test.db")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM budget")
    rows = cursor.fetchall()

    with open(csv_file, "w", newline='', encoding='utf-8') as f:  # Ouvrir en mode écriture ('w')
        writer = csv.writer(f)
        writer.writerow(["id", "name", "category", "price"])  #Ajout des en-têtes
        writer.writerows(rows)  #Écriture des données

    db.close()
    click.echo(f"Exportation réussie vers {csv_file}")  


@cli.command()
@click.option("-id" , )



if __name__ == "__main__":
    cli()    