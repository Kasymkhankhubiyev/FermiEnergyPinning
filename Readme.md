## Основные модули
 в **MainWindow.py** реализован основной интерфейс для взаимодействия с пользователем. 
 Пользователь может выбрать заранее подготовленный шаблон наиболее распространенных полпроводников, или ввести параметры вручную.
 При запуске программы по умолчанию заполнены данные для Кремния. Помимо ввода/выбора основных параметров нужно ввести параметры 
 энергетического уровня поверхностных акцепторов и величину внешнего поля.
 
 Значения параметров считываются упаковываются в словарь и передаются в функцию "*calculate*" из блока **calculations.py** на выходе получаем словарь с рассчетными данными в виде массивов и передаем в **DrawGraphs** для отрисовки.

в **DrawGraphs** реализуем отрисовку графиков.
Отрисовка графиков реализуется с помощью API:
*from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg*

не используем *pyplot*, т.к. из-за него возникают проблемы в runtime.
В частности, после уничтожения окна tk.Tk() висит процесс отрисовки в статичном режиме

в **SemiconductorsTemplates.py** реализованы шаблоны базовых данных о полупроводниках:
эффективные массы плотности состояний $m_{c}$ для электронов и $m_{v}$ для дырок,
ширина запрещенной зоны $E_{g}$, диэлектрическая пронициаемость $ε$.

Рассчет параметром в блоке **calculations.py**:
- Уровень Ферми рассчитывается с использованием библиотеки *fti-phompy* посредством метода *DopedSemiconductor*. Метод поиска уровня ферми расчитывается итеративным методом: Метод секущих берем серединное значение, для выбранного уровня ферми считаем заряды $n$, $p$, $N_d^+$. Рассчитывается суммарный заряд $Q = n - p - N_d^+$, 
считаем отночение суммарного заряда к кол-ву основных зарядов. Если отношение меньше десятой доли процента - выходим из цикла, если нет - делаем шаг интерации.
- если концентрация поверхностных акцепторов отлична от нуля, то рассчитываем величину изгиба зоны из трансцендентного уравнения итеративным методом: 
$$\sqrt{\frac{\epsilon\phi_{s}N_{d0}}{2\pi e^2}} = N_{as}\frac{1}{1 + e^\frac{E_{as}+\phi_{s}-E_{f}}{kT}} + \frac{E_out}{4\pi e}$$
если концентрация поверхностных акцепторов равно нулю, то выражаем изгиб зоны так: $$\phi_s = (\frac{E_{out}}{4\pi e})^2\frac{2\pi\epsilon_0}{\epsilon N_d e}$$
- Ширина ОПЗ расчитывается через уравнение: $$\sqrt{\frac{2\phi\epsilon\epsilon_0}{e^2N_d}}$$

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
$n = N_{C}\times e^\frac{E_{f}-E_{g}}{kT}$   $p = N_{V}\times e^\frac{-E_{f}}{kT}$

Доля заряженных доноров определяется положением уровня Ферми:
$N_{d}^+ = N_{d0}\frac{1}{1 + e^\frac{E_{g}-E{d}-E_{f}}{kT}}$

Положение уровня Ферми находится из уравнения: $N_{d}^+ + p = n$

Находим изгиб зон, когда нет внешнего поля, условие: заряд поверхностных акцепторов равен заряду ОПЗ.

Кол-во заряженных поверхностных акцепторов:
$N_{as}^+ = N_{as}\frac{1}{1 + e^\frac{E_{as}+\phi_{s}-E_{f}}{kT}}$, создаваемое ими поле $E_{as_{max}}^+$

Глубина ОПЗ при обеднении:
$W = \sqrt{\frac{\epsilon\phi_{s}}{2\pi e^2 N_{d}}}$, поверхностный заряд ОПЗ $N_{d0}We$

Изгиб зон $\phi_{s}$ ищем из равенства $\sqrt{\frac{\epsilon\phi_{s}N_{d0}}{2\pi e^2}} = N_{as}\frac{1}{1 + e^\frac{E_{as}+\phi_{s}-E_{f}}{kT}}$

При наличии внешнего поля $E_{out}$ уравнение принимает вид:
$\sqrt{\frac{\epsilon\phi_{s}N_{d0}}{2\pi e^2}} = N_{as}\frac{1}{1 + e^\frac{E_{as}+\phi_{s}-E_{f}}{kT}} + \frac{E_out}{4\pi e}$

## Расчет уровня Ферми:

Перед началом вычислений входные данные проверяются на допустимость.
1. Уровень поверхностных акцепторов должен быть внутри запрещенной зоны $E_{as} <= E_{g}$
2. Внешнее поле не превосходит внутренее поле создаваемое поверхностными акцепторами $U_{out} <= U_{as}$
3. Концентрация доноров не превосходит концентрацию основных носителей в валентной зоне и зоне проводимости $N_{d0} <= N_{c}$ и $N_{d0} <= N_{v}$

$\phi$ - корень уравнения
