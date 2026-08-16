Let me walk you through how I think about SOLID principles in day-to-day code.
SOLID isn't something I check off a list - it's more a set of habits that keep code easy to change later.
Single responsibility means a class should only have one reason to change.
If I find a class handling both business logic and formatting, that's usually a sign it's doing too much.
I split that kind of class into two - one that calculates the data, one that presents it.
The benefit is that a change in formatting doesn't risk breaking the calculation logic and vice versa.
A common mistake is splitting things too aggressively and ending up with classes that barely do anything on their own.
Open-closed principle means you should be able to extend behavior without modifying existing code.
I usually achieve that with interfaces or composition instead of editing a class that already works.
Instead of adding another if statement for a new payment type, I add a new class that implements the same interface.
That way the existing payment logic stays untouched and tested, and only the new class needs review.
The risk is over-engineering it upfront - I only add that flexibility once I actually see a second case coming.
Liskov substitution means a subclass should be usable wherever the base class is expected, without surprising behavior.
I've seen bugs where a subclass quietly changed what a method returned, which broke every caller that relied on the original contract.
A classic example is a square inheriting from a rectangle - resizing one side breaks the assumption that width and height are independent.
When I catch myself writing extra type checks for one specific subclass, that's usually a sign the hierarchy violates this principle.
Interface segregation means clients shouldn't be forced to depend on methods they don't actually use.
I prefer several small, focused interfaces over one large interface that tries to cover every use case.
A printer interface with scan and fax methods forces a simple printer class to implement things it doesn't support.
Splitting it into separate interfaces means each implementation only needs to satisfy what it actually does.
Dependency inversion means high-level modules shouldn't depend directly on low-level implementation details.
Both sides should depend on an abstraction, so the concrete implementation can change without touching the business logic.
In practice, I inject dependencies through the constructor instead of instantiating them inside the class.
That makes it easy to swap a real database for a mock in tests without changing any production code.
DRY is about avoiding duplicated knowledge, not just avoiding duplicated lines of code.
Two pieces of code can look identical today and still represent completely different business rules that happen to coincide.
If I merge those too early, a future change to one rule accidentally breaks the other.
Sometimes a little duplication is genuinely better than forcing the wrong abstraction onto two things that only look similar.
I usually wait until I see the same logic a third time before I extract it into a shared function.
KISS means choosing the simplest solution that actually solves the problem in front of you.
I've seen simple CRUD features built with layers of abstraction that were only needed for far more complex systems.
Complexity that isn't paying for itself just slows down every future change to that code.
YAGNI reminds me not to build flexibility for requirements that don't exist yet.
It's tempting to add configuration options just in case, but each one adds a path that needs testing and maintaining forever.
I'd rather ship the simple version now and refactor later if a second real use case actually shows up.
I think design patterns are tools, not goals - I only reach for one when it actually fits the problem.
Naming the pattern you're using also makes code reviews faster, because the reviewer immediately recognizes the shape of the solution.
Overusing patterns can add more complexity than the problem they're supposed to solve.
I use the factory pattern when object creation logic gets too complex to just call a constructor directly.
If creating an object depends on configuration or the type of input, a factory function keeps that logic in one place.
It also means callers don't need to know which concrete class they're getting back.
The strategy pattern lets me swap out an algorithm at runtime without changing the code that calls it.
A good example is choosing between different pricing strategies based on a setting, instead of a long chain of if statements.
Each strategy becomes its own small class, which is easy to test in isolation.
I reach for the observer pattern when multiple parts of the app need to react to the same event.
A typical case is a UI component that needs to update whenever some shared state changes elsewhere in the app.
It keeps the thing that changes decoupled from the things that react to the change.
The decorator pattern is useful when I need to add behavior to an object without changing its original class.
For example, wrapping an API client with logging or caching without touching the original request logic.
It also lets me combine several of these wrappers together in different combinations depending on what's needed.
The adapter pattern helps when I need to make an incompatible interface work with existing code.
I used it recently to wrap a third-party library so the rest of the app could keep talking to our own interface.
That way, if we ever replace the third-party library, only the adapter needs to change.
I avoid singletons in most cases because they introduce hidden shared state and make testing harder.
Once something is a singleton, it's difficult to mock or reset between tests without leaking state across them.
If I genuinely need a single shared instance, I'd rather pass it in explicitly than rely on global access.
Dependency injection is how I keep business logic separate from infrastructure concerns like databases or external APIs.
Instead of a class creating its own dependencies, they're passed in from the outside, usually through the constructor.
That makes the class easier to test, because I can pass in a fake implementation instead of the real one.
When I review code, I look for repeated logic that could become a shared function, but I don't force it prematurely.
Good abstractions come from real repetition I've actually seen, not from guessing what might repeat in the future.
I try to favor composition over inheritance, because it's easier to change behavior by swapping a dependency than by rewriting a class hierarchy.
A tightly coupled codebase is harder to test, harder to change, and harder to reason about, even if each individual class looks fine.
At the end of the day, all of these principles exist to make future changes cheaper, not to satisfy some abstract rule.
Another question I get asked a lot is the difference between imperative and declarative code.
Imperative code tells the computer exactly how to do something, step by step.
A for loop that manually checks each item and pushes the matching ones into a new array is a classic imperative example.
Declarative code describes what result you want and lets the underlying system figure out how to get there.
Calling the array's filter method instead of writing that loop by hand is the declarative equivalent of the same task.
Manually creating DOM nodes with document.createElement and updating them by hand is an imperative way of building a UI.
Writing JSX that describes what the UI should look like for a given state is a declarative way of building the same UI.
React itself is declarative - you describe the UI you want, and React works out how to update the actual DOM.
SQL is declarative too - you describe what data you want, not the exact steps the database should take to fetch it.
GraphQL queries are declarative in the same way - the client describes the shape of the data it needs, not how to retrieve it.
Infrastructure as code tools like Terraform are declarative - you describe the desired end state, not the commands to reach it.
Declarative code tends to be easier to read, because it hides the how and only shows the what.
The trade-off is that declarative code can be harder to debug, since you don't control the exact steps being executed underneath.
Imperative code gives you more control, which matters when you actually need to optimize something by hand.
In practice I mix both - business logic tends to stay imperative, while UI rendering and data transforms are usually declarative.
Array methods like map, filter, and reduce let me write declarative transformations instead of manual loops with index variables.
Even in a declarative pipeline, I still need to understand what's happening underneath it when something goes wrong.
I default to declarative style whenever I can, because it's usually easier for teammates to read and reason about later.
Deterministic and non-deterministic is another distinction that comes up, especially around testing.
Deterministic means that given the same input, the code always produces exactly the same output.
A pure function that just adds two numbers together is deterministic - there's nothing outside it that can change the result.
Non-deterministic means the same input can produce different outputs, because something outside the function affects the result.
Calling Math.random or reading the current date makes a function non-deterministic, since the result depends on when or how it runs.
A network call is non-deterministic too - the response can vary, arrive late, or fail entirely, even with the exact same request.
Deterministic code is much easier to test, because I can assert on one expected result without worrying about edge cases.
Non-deterministic code is harder to test, so I usually mock the source of randomness or time to make the test predictable.
Race conditions are a common source of non-determinism, since the order in which things finish isn't guaranteed.
A database query without an explicit order can return rows in a different sequence each time it runs.
I try to keep the core business logic deterministic and push things like randomness or the current time out to the edges of the system.
In distributed systems, network delays and retries introduce non-determinism that I have to design around rather than avoid entirely.
A flaky test that fails only sometimes is usually a sign that some non-deterministic behavior wasn't properly isolated.
When I need reproducible results in tests, I seed the random generator or freeze the clock instead of using the real one.
Caching can also introduce non-determinism, since the cached value and the real source of truth can drift out of sync over time.
