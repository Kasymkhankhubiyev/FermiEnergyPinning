## Основные модули
 в **MainWindow.py** реализован основной интерфейс для взаимодействия с пользователем

в **DrawGraphs** реализуем логику отрисовки графиков.
Отрисовка графиков реализуется с помощью API:
*from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg*

не используем *pyplot*, т.к. из-за него возникают проблемы в runtime.
В частности, после уничтожения окна tk.Tk() висит процесс отрисовки в статичном режиме

в **SemiconductorsTemplates.py** реализованы шаблоны базовых данных о полупроводниках:
эффективные массы плотности состояний $m_{c}$ для электронов и $m_{v}$ для дырок,
ширина запрещенной зоны $E_{g}$, диэлектрическая пронициаемость $ε$.

## Входные данные:
На вход программа получает данные - параметры полупроводника: 
- Запрещенная зона $E_{g}$
- Диэлектрическая пронициаемость $ε$
- Эффективные массы плотности состояний в долинах для дырок $m_{v}$
и для электронов $m_{c}$
- Положение уровня донора $E_{d}$
- Концентрация доноров $N_{d0}$
- Температура $T$
- Плотность поверхностных акцепторов $N_{as}$
- Положение уровня энергии акцепторов $E_{as}$
- Внешнее поле $E_{out} [V/m]$

**Все энергии отсчитываются от потолка валентной зоны
Только энергия донора вниз от дна зоны проводимости!**

## Формулы:

Сначала находим эффективную плотность состояний электронов и дырок:
$N_{C(V)} = 2.51\times10^9\times(\frac{m_{c(v)}}{m_{0}})^\frac{3}{2}(\frac{T}{300})^\frac{3}{2}\times cm^-3$

Положение уровня Ферми в квазинейтральном объеме находим из электронейтральности:
$n = N_{C}\times e^\frac{E_{f}-E_{g}}{kT}   p = N_{V}\times e^\frac{-E_{f}}{kT}$

Доля заряженных доноров определяется положением уровня Ферми:
$N_{d}^+ = N_{d0}\frac{1}{1 + e^\frac{E_{g}-E{d}-E_{f}}{kT}}$

Положение уровня Ферми находится из уравнения: $N_{d}^+ + p = n$

Находим изгиб зон, когда нет внешнего поля, условие: заряд поверхностных акцепторов равен заряду ОПЗ.

Кол-во заряженных поверхностных акцепторов:
$N_{as}^+ = N_{as}\frac{1}{1 + e^\frac{E_{as}+\phi_{s}-E_{f}}{kT}}$, создаваемое ими поле $E_{as_{max}}^+$

Глубина ОПЗ при обеднении:
$W = \sqrt{\frac{\epsilon\phi_{s}}{2\pi e^2 N_{d}}}$, поверхностный заряд ОПЗ $N_{d0}We$

Изгиб зон $\phi_{s}$ ищем из равенства $\sqrt{\frac{\epslon\phi_{s}N_{d0}}{2\pi e^2}} = N_{as}\frac{1}{1 + e^\frac{E_{as}+\phi_{s}-E_{f}}{kT}}$

При наличии внешнего поля $E_{out}$ уравнение принимает вид:
$\sqrt{\frac{\epslon\phi_{s}N_{d0}}{2\pi e^2}} = N_{as}\frac{1}{1 + e^\frac{E_{as}+\phi_{s}-E_{f}}{kT}} + \frac{E_out}{4\pi e}$
