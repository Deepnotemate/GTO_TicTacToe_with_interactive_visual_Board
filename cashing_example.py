"""
SUPER SIMPLE CACHING EXAMPLE FOR DUMMIES
=========================================
Was ist schlecht: Die gleiche Berechnung mehrfach machen
Was ist gut: Ergebnis speichern und wiederverwenden!
"""

# ============================================================
# BEISPIEL 1: OHNE CACHE (LANGSAM!)
# ============================================================

print("=" * 60)
print("BEISPIEL 1: OHNE CACHE")
print("=" * 60)

def fib_ohne_cache(n):
    """Berechne die n-te Fibonacci-Zahl (sehr langsam!)"""
    print(f"  Berechne fib({n})")  # Zeige was berechnet wird
    
    if n <= 1:
        return n
    return fib_ohne_cache(n - 1) + fib_ohne_cache(n - 2)

# Teste es
print("\nBerechne fib(5) ohne Cache:")
result = fib_ohne_cache(5)
print(f"Ergebnis: {result}")
print("\n⚠️  Bemerkt wie oft die gleichen Nummern berechnet werden?")
print("Berechne fib(5) nochmal:")
result = fib_ohne_cache(5)  # ALLES wird nochmal berechnet! 😭


# ============================================================
# BEISPIEL 2: MIT CACHE (SCHNELL!)
# ============================================================

print("\n" + "=" * 60)
print("BEISPIEL 2: MIT CACHE")
print("=" * 60)

class CachedFibonacci:
    """Fibonacci mit Caching"""
    
    def __init__(self):
        # Der Cache: speichert n → ergebnis
        self.cache = {}
    
    def calculate(self, n):
        """Berechne fib(n) mit Caching"""
        
        # SCHRITT 1: Check ob wir das schon berechnet haben
        if n in self.cache:
            print(f"  ✅ Cache HIT! fib({n}) = {self.cache[n]} (nicht neu berechnet!)")
            return self.cache[n]
        
        # SCHRITT 2: Wenn nicht im Cache → berechne
        print(f"  🔄 Berechne fib({n})")
        
        if n <= 1:
            result = n
        else:
            result = self.calculate(n - 1) + self.calculate(n - 2)
        
        # SCHRITT 3: Speichere im Cache für später
        self.cache[n] = result
        print(f"  💾 Speichere fib({n}) = {result} im Cache")
        
        return result

# Teste es
fib_cached = CachedFibonacci()

print("\nBerechne fib(5) mit Cache (1. Mal):")
result1 = fib_cached.calculate(5)
print(f"Ergebnis: {result1}")

print("\n" + "-" * 60)
print("Berechne fib(5) mit Cache (2. Mal):")
result2 = fib_cached.calculate(5)
print(f"Ergebnis: {result2}")
print("\n✨ Viel schneller! Alles kommt aus dem Cache!")

print(f"\nCache Inhalt: {fib_cached.cache}")


# ============================================================
# BEISPIEL 3: VISUALISIERUNG MIT VARIABLEN
# ============================================================

print("\n" + "=" * 60)
print("BEISPIEL 3: WAS PASSIERT IM CACHE")
print("=" * 60)

cache = {}

# Simuliere 3 Variablen die wir cachen
var1 = [1, 2, 3]
var2 = [4, 5, 6]
var3 = [1, 2, 3]  # Gleicher Inhalt wie var1!

print("\n❌ PROBLEM: Lists sind nicht hashbar!")
print("Das geht nicht:")
try:
    cache[var1] = "Ergebnis 1"  # Würde crashen
except TypeError as e:
    print(f"   TypeError: {e}")

print("\n✅ LÖSUNG: Tuple verwenden (hashbar!)")
tuple1 = tuple(var1)      # (1, 2, 3)
tuple2 = tuple(var2)      # (4, 5, 6)
tuple3 = tuple(var3)      # (1, 2, 3)

# Jetzt geht's!
cache[tuple1] = "Ergebnis 1"
cache[tuple2] = "Ergebnis 2"
cache[tuple3] = "Ergebnis 3"

print(f"\nCache nach 3 'Berechnungen':")
print(f"{cache}")

print(f"\nAnzahl Einträge: {len(cache)}")
print("❓ Warum nur 2 Einträge statt 3?")
print(f"   Weil tuple1 und tuple3 identisch sind: (1, 2, 3)")
print(f"   tuple3 überschrieb tuple1 im Cache!")

print("\n" + "=" * 60)
print("ZUSAMMENFASSUNG")
print("=" * 60)
print("""
1. Cache speichert: Input → Ergebnis
   cache[input] = result

2. Unhashable (List)  → kann nicht als Key sein
   Hashable (Tuple)   → kann als Key sein

3. Vorher: Gleiche Berechnung 10x gemacht
   Nachher: 1x berechnet, 9x aus Cache geholt ⚡

4. In TicTacToe:
   Input:  (board_tuple, is_human)
   Output: (score, best_board)
   
   Wenn die gleiche Board-Position nochmal auftritt:
   → Sofort aus Cache, nicht neu berechnet!
""")
