# IELTS Writing roadmap — l2-vocab

`l2-vocab` почалась як реактивна фіксація слів з курсу ESOL L2 Writing/Reading.
Переглянувши всю `cards.yaml`, видно, що дека вже — без свідомого плану —
з'їхала в бік IELTS Writing: граматичні конструкції формального письма
(inversion, `each of/either of/neither of`, узгодження з collective nouns,
конектори), IELTS Writing Task 1 Academic (опис bar/pie/line charts),
IELTS Writing Task 2 (essay hooks, лінкери) і навіть IELTS Writing Task 1
General Training (формальний лист).

Цей документ фіксує це свідомо: яку навичку тренує дека, що вже покрито
(щоб не дублювати), і що додавати далі — за пріоритетом.

---

## 1. Яку навичку тренує дека

Формат картки — це UA-промпт → надрукована EN-відповідь + аудіо з `Back`.

| навичка | як тренується |
|---------|----------------|
| **Writing** | основна — продукція речення з нуля, це і є суть картки |
| **Listening** | побічно — через прослуховування Audio при повторенні |
| **Reading** | дотично — лише через словниковий запас, не через сам формат картки |
| **Speaking** | дотично — ті самі конструкції/лексика придатні для усного мовлення |

Тип іспиту поки не визначений — **Academic і General Training обидва в
скоупі**, тому roadmap тримає окремі гілки для Task 1 Academic (графіки) і
Task 1 General Training (лист).

---

## 2. Ключ — позначення, які вже використовуються у `Front`

Щоб нові картки лишались консистентними зі старими:

| позначення | значення |
|------------|----------|
| `(варіант1\|варіант2)` | синонім-підказка — вибір слів для перекладу |
| `~нотатка~` | нюанс/реєстр/відтінок значення прив'язаного слова |
| `<b>...</b>` | акцент на ключовому структурному елементі речення |
| `[PrCont]`, `[PrPerf]`, `(PrCont)` тощо | тег часу/форми, яку картка тренує |

`Front` = українською, `Back` = очікувана англійська відповідь, `Audio` =
TTS з `Back` (генерується `generate_audio.py`).

---

## 3. Аудит — що вже є в деці

Щоб не додавати дублі. Категорії виведені з перегляду всіх ~210 карток.

### 3.1 Тематична лексика в реченнях
economy, education/literacy, critical thinking, reading habits/culture,
engagement, volunteering, crypto, environment/recycling, remote work, AI,
COVID-19/pandemic, war in Ukraine.

### 3.2 Граматичні конструкції для письма
- Inversion patterns (`Only after`, `Never`, `Not until`, `Hardly`...)
- Cleft sentences, conditional inversion (`Were I you...`, `Had he known...`)
- `each of / either of / neither of / not only... but also`
- Узгодження з collective nouns (`the government is/are`, `the team have`)
- Псевдо-множина підмета (`along with`, `together with`, `as well as`)
- Лінкери контрасту/додавання (`however`, `nevertheless`, `moreover`,
  `furthermore`)

### 3.3 IELTS Task 1 Academic
Опис bar chart / pie chart / line graph: overview-речення, опис тренду,
порівняння (`by contrast`, `in contrast`). **Тільки ці 3 типи графіків.**

### 3.4 IELTS Task 2 essay
Гачки-відкривачки (риторичне питання, `Imagine a world...`, `Few issues
have attracted...`), thesis-statement речення, контраст через крапку з
комою (`...; however, ...`).

### 3.5 IELTS Task 1 General Training
Формальний лист — але лише в тоні suggestion/complaint: `It may also be
worth considering...`, `I would be grateful if...`, `I look forward to
hearing from you at your earliest convenience`.

---

## 4. Roadmap — що додавати далі (за пріоритетом)

### A. Task 1 Academic — типи графіків, яких ще немає
- [ ] Table description language
- [ ] Maps / process diagrams (просторова + послідовна лексика: `to the
  north of`, `is followed by`, `converted into`)
- [ ] Multi-chart comparison (два графіки в одному завданні)
- [ ] Precision-of-change лексика — див. `docs/ielts-trends.md`
  (напрям, магнітуда, швидкість, стабільність, коливання, піки,
  порівняння двох ліній, граматика прийменників, готові шаблони речень)
- [ ] Paraphrasing вступного речення (перефразування питання завдання)

### B. Task 1 General Training — типи листів, яких ще немає
- [ ] Request letter
- [ ] Invitation letter
- [ ] Apology / explanation letter
- [ ] Informal letter (до друга — GT інколи вимагає неформальний регістр;
  наразі все, що є, формальне — це найбільша прогалина)
- [ ] Opening lines за типом листа (`I am writing to inform/request/
  apologise/enquire about...`)

### C. Task 2 — структури есе
- [ ] Topic-sentence + body-paragraph патерни для кожного типу есе: opinion
  essay, discussion (both views), advantage/disadvantage, problem/solution,
  two-part question (наразі є лише вступні гачки, немає структури тіла)
- [ ] Conclusion phrases — їх ще немає взагалі (`In conclusion...`,
  `Taking everything into account...`, `On balance...`)
- [ ] Hedging / academic caution окремим блоком (зараз трапляється хаотично
  через нотатки `~50%~`) — формалізувати: `may/might/tends to/arguably/
  it could be argued that`

### D. Нові теми Task 2, яких ще не було
Crime & punishment, globalization, urbanization, tourism, advertising,
gender equality, immigration, media, sport & health, government spending
priorities, technology & privacy.

### E. Словник/колокації (вторинне — але живить і Reading, і Speaking)
Див. `docs/ielts-vocab.md` — самостійно дібраний, організований по темах
Task 2 з розділу D, публічні word-list'и використані лише як чек-лист
покриття, а не імпортовані напряму.

---

## 5. Рекомендований порядок роботи

1. Добити Task 1 Academic — покрити всі типи графіків (A)
2. Заповнити Task 1 GT — типи листів, особливо informal register (B)
3. Task 2 — структура тіла есе + conclusions (C)
4. Нові теми Task 2 (D)
5. Колокації — паралельно, підмішувати в інші блоки (E)
