from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from app1.models import CardData, Deck, DeckEntry, Collection, CollectionEntry
from app1.forms import SearchCardForm, JoinForm, LoginForm
import requests
from pokemontcgsdk import Card
from .utils.gemini import getDeckStrategy
from django.contrib import messages


@login_required(login_url="/login/")
def home(request):
    return render(request, "app1/home.html")


@login_required(login_url="/login/")
def modifyDeck(request):
    page_data = {"search_card_form": SearchCardForm}

    if request.method == "POST":
        if "delete" in request.POST:
            card_name = request.POST.get("card-name")
            card_number = request.POST.get("card-number")

            try:
                deck = Deck.objects.get(user=request.user)
                card = CardData.objects.get(name=card_name, number=card_number)
                entry = DeckEntry.objects.get(deck=deck, card=card)

                if entry.count > 1:
                    entry.count -= 1
                    entry.save()
                else:
                    entry.delete()

                page_data["entries"] = deck.entries.all()

                return redirect("/deck/")
            except (
                Deck.DoesNotExist,
                CardData.DoesNotExist,
                DeckEntry.DoesNotExist,
            ):
                messages.error(request, "Error deleting card")

            return render(request, "app1/deck.html", page_data)

        search_card_form = SearchCardForm(request.POST)

        if search_card_form.is_valid():
            card_name = search_card_form.cleaned_data["card_name"].strip()
            card_name = card_name[0].upper() + card_name[1:]

            set_name = search_card_form.cleaned_data["set_name"].strip()
            set_name = set_name[0].upper() + set_name[1:]

            card_number = search_card_form.cleaned_data["card_number"].strip()

            card = getCardData(card_name, set_name, card_number)

            if not card:
                try:
                    page_data["entries"] = Deck.objects.get(
                        user=request.user
                    ).entries.all()

                    return redirect("/deck/")
                except Deck.DoesNotExist:
                    messages.error(request, "Error adding card, deck does not exist")

                return render(request, "app1/deck.html", page_data)

            try:
                deck = Deck.objects.get(user=request.user)

                try:
                    DeckEntry.objects.get(deck=deck, card=card).count += 1
                    DeckEntry.objects.get(deck=deck, card=card).save()
                except DeckEntry.DoesNotExist:
                    DeckEntry(deck=deck, card=card).save()

                page_data["entries"] = deck.entries.all()

                return redirect("/deck/")
            except Deck.DoesNotExist:
                deck = Deck(user=request.user)
                deck.save()

                try:
                    DeckEntry.objects.get(deck=deck, card=card).count += 1
                    DeckEntry.objects.get(deck=deck, card=card).save()
                except DeckEntry.DoesNotExist:
                    DeckEntry(deck=deck, card=card).save()

                page_data["entries"] = deck.entries.all()

                return redirect("/deck/")
        else:
            page_data["search_card_form"] = search_card_form

    try:
        page_data["entries"] = Deck.objects.get(user=request.user).entries.all()
    except Deck.DoesNotExist:
        messages.error(request, "Create a deck to view cards")

    return render(request, "app1/deck.html", page_data)


@login_required(login_url="/login/")
def modifyCollection(request):
    page_data = {"search_card_form": SearchCardForm}

    if request.method == "POST":
        if "delete" in request.POST:
            card_name = request.POST.get("card-name")
            card_number = request.POST.get("card-number")

            try:
                collection = Collection.objects.get(user=request.user)
                card = CardData.objects.get(name=card_name, number=card_number)
                entry = CollectionEntry.objects.get(collection=collection, card=card)

                if entry.count > 1:
                    entry.count -= 1
                    entry.save()
                else:
                    entry.delete()

                page_data["entries"] = collection.entries.all()
                page_data["count"] = len(page_data["entries"])

                return redirect("/collection/")
            except (
                Collection.DoesNotExist,
                CardData.DoesNotExist,
                CollectionEntry.DoesNotExist,
            ):
                messages.error(request, "Error deleting card")

            return render(request, "app1/collection.html", page_data)

        search_card_form = SearchCardForm(request.POST)

        if search_card_form.is_valid():
            card_name = search_card_form.cleaned_data["card_name"].strip()
            card_name = card_name[0].upper() + card_name[1:]

            set_name = search_card_form.cleaned_data["set_name"].strip()
            set_name = set_name[0].upper() + set_name[1:]

            card_number = search_card_form.cleaned_data["card_number"].strip()

            card = getCardData(card_name, set_name, card_number)

            if not card:
                try:
                    page_data["entries"] = Collection.objects.get(
                        user=request.user
                    ).entries.all()
                    page_data["count"] = len(page_data["entries"])

                    return redirect("/collection/")
                except Collection.DoesNotExist:
                    messages.error(
                        request, "Error creating card, collection does not exist"
                    )

                return render(request, "app1/collection.html", page_data)

            try:
                collection = Collection.objects.get(user=request.user)

                try:
                    CollectionEntry.objects.get(
                        collection=collection, card=card
                    ).count += 1
                    CollectionEntry.objects.get(collection=collection, card=card).save()
                except CollectionEntry.DoesNotExist:
                    CollectionEntry(collection=collection, card=card).save()

                page_data["entries"] = collection.entries.all()
                page_data["count"] = len(page_data["entries"])

                return redirect("/collection/")
            except Collection.DoesNotExist:
                collection = Collection(user=request.user)
                collection.save()

                try:
                    CollectionEntry.objects.get(
                        collection=collection, card=card
                    ).count += 1
                    CollectionEntry.objects.get(collection=collection, card=card).save()
                except CollectionEntry.DoesNotExist:
                    CollectionEntry(collection=collection, card=card).save()

                page_data["entries"] = collection.entries.all()
                page_data["count"] = len(page_data["entries"])

                return redirect("/collection/")
        else:
            page_data["search_card_form"] = search_card_form

    try:
        page_data["entries"] = Collection.objects.get(user=request.user).entries.all()
        page_data["count"] = len(page_data["entries"])
    except Collection.DoesNotExist:
        messages.error(request, "Create a collection to view cards")

    return render(request, "app1/collection.html", page_data)


def getCardData(card_name, set_name, card_number):
    query = []

    if card_name:
        query.append(f'name:"{card_name}"')
    if set_name:
        query.append(f'set.name:"{set_name}"')

    query = " ".join(query)
    cards = Card.where(q=query)
    card_data = None

    if not cards:
        messages.error("Card could not be found, enter card information again")
        return None

    for card in cards:
        if card.name == card_name and card.number == card_number:
            card_data = card
            break

    if not card_data:
        return None

    prices = {}
    if card_data.tcgplayer.prices:
        if card_data.tcgplayer.prices.normal:
            prices["low"] = card_data.tcgplayer.prices.normal.low
            prices["mid"] = card_data.tcgplayer.prices.normal.mid
            prices["high"] = card_data.tcgplayer.prices.normal.high
        elif card_data.tcgplayer.prices.holofoil:
            prices["low"] = card_data.tcgplayer.prices.holofoil.low
            prices["mid"] = card_data.tcgplayer.prices.holofoil.mid
            prices["high"] = card_data.tcgplayer.prices.holofoil.high

    if card_data.supertype == "Pokémon":
        abilities = {}
        if card_data.abilities:
            for ability in card_data.abilities:
                abilities[ability.name] = ability.text

        attacks = {}
        if card_data.attacks:
            for attack in card_data.attacks:
                attacks[attack.name] = {
                    "cost": attack.cost,
                    "damage": attack.damage,
                    "description": attack.text,
                }

        weaknesses = {}
        if card_data.weaknesses:
            for weakness in card_data.weaknesses:
                weaknesses[weakness.type] = weakness.value

        resistances = {}
        if card_data.resistances:
            for resistance in card_data.resistances:
                resistances[resistance.type] = resistance.value

        card_data = CardData(
            id=card_data.id,
            name=card_data.name,
            number=card_number,
            type=card_data.supertype,
            image=card_data.images.large,
            prices=prices,
            hp=card_data.hp,
            types=card_data.types,
            abilities=abilities,
            attacks=attacks,
            weaknesses=weaknesses,
            resistances=resistances,
            retreat=card_data.convertedRetreatCost,
        )
        card_data.save()

        return card_data
    elif card_data.supertype == "Trainer" or card_data.supertype == "Energy":
        card_data = CardData(
            id=card.id,
            name=card.name,
            number=card_number,
            type=card.supertype,
            image=card.images.large,
            prices=prices,
            rules=card.rules,
        )
        card_data.save()

        return card_data


@login_required(login_url="/login/")
def generateStrategy(request):
    if request.method == "POST":
        try:
            deck = Deck.objects.get(user=request.user)
            entries = "\n".join(
                [
                    f"{entry.count}x {entry.card.name} ({entry.card.number})"
                    for entry in deck.entries.all()
                ]
            )
            strategy = getDeckStrategy(entries)

            return JsonResponse({"strategy": strategy})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


def about(request):
    return render(request, "app1/about.html")


def rules(request):
    return render(request, "app1/rules.html")


def serverInfo(request):
    server_geodata = requests.get("https://ipwhois.app/json/").json()
    settings_dump = settings.__dict__

    return HttpResponse("{}{}".format(server_geodata, settings_dump))


def userJoin(request):
    if request.method == "POST":
        join_form = JoinForm(request.POST)

        if join_form.is_valid():
            user = join_form.save()
            user.set_password(user.password)
            user.save()

            return redirect("/login/")
        else:
            page_data = {"join_form": join_form}

            return render(request, "app1/join.html", page_data)
    else:
        page_data = {"join_form": JoinForm}

        return render(request, "app1/join.html", page_data)


def userLogin(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)

            if user:
                if user.is_active:
                    login(request, user)

                    return redirect("/")
                else:
                    return HttpResponse("Your account is not active.")
            else:
                print("Someone tried to login and failed.")
                print(
                    "They used username: {} and password: {}".format(username, password)
                )

                return render(request, "app1/login.html", {"login_form": LoginForm})
        else:
            print("Login form is not valid.")

            return render(request, "app1/login.html", {"login_form": LoginForm})
    else:
        return render(request, "app1/login.html", {"login_form": LoginForm})


@login_required(login_url="/login/")
def userLogout(request):
    logout(request)

    return redirect("/login/")
