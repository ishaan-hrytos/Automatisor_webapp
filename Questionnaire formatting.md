

\---

# About the company & site

Name of the company:  
Location of the site:  
Square footage:

\#\# SECTION 01 — PHYSICAL ENVIRONMENT

\#\#\# Q1 – Aisle Width  
\*\*Field ID:\*\* \`aisle\_width\`  
\*\*Type:\*\* Single select  
\*\*Required:\*\* YES — blocks scoring if unanswered  
\*\*Question:\*\* What is the typical aisle width in the main internal transport zones?

| Option | Value |  
|--------|-------|  
| Under 7 ft (very narrow aisle) | \`under\_7ft\` |  
| 7 – 10 ft (narrow aisle) | \`7\_10ft\` |  
| 10 – 15 ft (standard aisle) | \`10\_15ft\` |  
| 15 – 20 ft (wide aisle) | \`15\_20ft\` |  
| Over 20 ft (very wide / open floor) | \`over\_20ft\` |

\#\#\# Q2 — Floor Surface Condition  
\*\*Field ID:\*\* \`floor\_condition\`  
\*\*Type:\*\* Single select  
\*\*Required:\*\* NO — if unanswered, apply conservative default (\`mixed\`) and flag  
\*\*Note:\*\* Confirm on site visit. Answer from desk research if available.  
\*\*Question:\*\* How would you describe the floor surface condition?

| Option | Value |  
|--------|-------|  
| Excellent – smooth, level, recently resurfaced | \`excellent\` |  
| Good – minor cracks or control joints, well maintained | \`good\` |  
| Fair – uneven sections, surface damage present | \`fair\` |  
| Poor – significant unevenness, heavy traffic damage | \`poor\` |  
| Mixed – varies significantly by zone | \`mixed\` |  
| Unknown at this stage | \`unknown\` |

\---

\#\#\# Q3 — Temperature Zone Exposure  
\*\*Field ID:\*\* \`temp\_exposure\`  
\*\*Type:\*\* Single select  
\*\*Required:\*\* NO — if unanswered, default to \`ambient\_only\`  
\*\*Question:\*\* Are cold or temperature-controlled zones present, and do  
transport operatives work in them?

| Option | Value |  
|--------|-------|  
| No – ambient only | \`ambient\_only\` |  
| Cold zones present but transport is ambient-side only | \`cold\_present\_ambient\_transport\` |  
| Transport operatives regularly work in refrigerated zones (35–46°F) | \`refrigerated\_exposure\` |  
| Transport operatives regularly work in freezer zones (0°F or below) | \`freezer\_exposure\` |  
| Both refrigerated and freezer zones with sustained operative exposure | \`both\_cold\_exposure\` |

\---

\#\# SECTION 02 — MATERIAL MOVEMENT

\#\#\# Q4 — Travel Distance  
\*\*Field ID:\*\* \`travel\_distance\`  
\*\*Type:\*\* Single select  
\*\*Required:\*\* YES — blocks scoring if unanswered  
\*\*Question:\*\* What is the typical one-way travel distance for the most  
frequent internal material moves?

| Option | Value |  
|--------|-------|  
| Under 100 ft | \`under\_100ft\` |  
| 100 – 250 ft | \`100\_250ft\` |  
| 250 – 500 ft | \`250\_500ft\` |  
| 500 – 1,000 ft | \`500\_1000ft\` |  
| Over 1,000 ft | \`over\_1000ft\` |

\---

\#\#\# Q5 — Primary Load Format  
\*\*Field ID:\*\* \`load\_format\`  
\*\*Type:\*\* Single select  
\*\*Required:\*\* NO — if unanswered, default to \`pallets\`  
\*\*Question:\*\* What is the primary load format being moved internally?

| Option | Value |  
|--------|-------|  
| Pallets (standard GMA / CHEP 48×40 in) | \`pallets\` |  
| Roll cages or dollies | \`roll\_cages\` |  
| Totes / bins / KLT containers | \`totes\` |  
| Large containers (IBCs, bulk) | \`large\_containers\` |  
| Mixed – multiple load formats in use | \`mixed\` |

\---

\#\#\# Q6 — Load Weight  
\*\*Field ID:\*\* \`load\_weight\`  
\*\*Type:\*\* Single select  
\*\*Required:\*\* NO — if unanswered, default to \`220\_660lbs\`  
\*\*Question:\*\* What is the average gross weight per load unit?

| Option | Value |  
|--------|-------|  
| Under 220 lbs | \`under\_220lbs\` |  
| 220 – 660 lbs | \`220\_660lbs\` |  
| 660 – 1,300 lbs | \`660\_1300lbs\` |  
| 1,300 – 2,200 lbs | \`1300\_2200lbs\` |  
| Over 2,200 lbs | \`over\_2200lbs\` |

\---

\#\# SECTION 03 — INFRASTRUCTURE & CONSTRAINTS

\#\#\# Q7 — WiFi / Network Infrastructure  
\*\*Field ID:\*\* \`wifi\_state\`  
\*\*Type:\*\* Single select  
\*\*Required:\*\* NO — if unanswered, default to \`unknown\`  
\*\*Note:\*\* Confirm on site visit. May be available from IT/facilities documentation.  
\*\*Question:\*\* What is the state of the warehouse WiFi / network infrastructure?

| Option | Value |  
|--------|-------|  
| Enterprise-grade WiFi 6 with full facility coverage | \`wifi6\_full\` |  
| Good coverage with some identified dead spots | \`good\_with\_gaps\` |  
| Patchy – unreliable in multiple zones | \`patchy\` |  
| Poor – limited or inconsistent coverage | \`poor\` |  
| No WiFi infrastructure in place | \`none\` |  
| Unknown at this stage | \`unknown\` |

\---

\#\#\# Q8 — Known Deployment Constraints  
\*\*Field ID:\*\* \`deployment\_constraints\`  
\*\*Type:\*\* Multi-select  
\*\*Required:\*\* NO  
\*\*Question:\*\* Are there any known physical constraints that would  
complicate tugger deployment?

| Option | Value |  
|--------|-------|  
| Narrow or irregular aisles in key transport zones | \`narrow\_aisles\` |  
| Floor surface conditions requiring remediation | \`floor\_remediation\` |  
| Restricted dock areas limiting approach or turning space | \`restricted\_docks\` |  
| Ramps, inclines, or multi-level transitions on transport routes | \`ramps\_inclines\` |  
| High-density pedestrian zones with no feasible segregation path | \`pedestrian\_conflict\` |  
| No significant physical constraints identified | \`none\` |

\---

\#\# SECTION 04 — TRANSPORT OPERATION

\#\#\# Q9 — Primary MHE Type  
\*\*Field ID:\*\* \`primary\_mhe\_type\`  
\*\*Type:\*\* Single select  
\*\*Required:\*\* NO — if unanswered, default to \`unknown\`  
\*\*Note:\*\* The equipment currently used for internal material transport determines  
displacement potential. Manual push equipment is the strongest tugger candidate.  
Powered equipment indicates the operation is already mechanised to some degree.  
\*\*Question:\*\* What is the primary equipment used for internal material transport  
(moving loads between zones, not picking or putaway)?

| Option | Value |  
|--------|-------|  
| Manual push – hand pallet jacks or carts (no powered equipment) | \`manual\_push\` |  
| Walkie / walkie-rider pallet jack | \`walkie\_rider\` |  
| Counterbalance forklift | \`counterbalance\_forklift\` |  
| Reach truck or narrow-aisle truck | \`reach\_truck\` |  
| Tugger trains or tow tractors (already in use) | \`tugger\_existing\` |  
| Mixed – multiple equipment types on different routes | \`mixed\` |  
| Unknown at this stage | \`unknown\` |

\---

\#\#\# Q10 — Transport FTE Count  
\*\*Field ID:\*\* \`transport\_ftes\`  
\*\*Type:\*\* Single select  
\*\*Required:\*\* NO — if unanswered, no boost applied; flag for follow-up  
\*\*Note:\*\* Count only operatives whose primary duty is internal material transport  
(forklift drivers, material handlers, tugger operators, picker-runners).  
Exclude pickers, packers, receivers, and supervisors. Count across all shifts.  
\*\*Question:\*\* How many FTEs are primarily dedicated to internal material transport  
at this site (across all shifts)?

| Option | Value |  
|--------|-------|  
| Fewer than 3 FTEs | \`under\_3\` |  
| 3 – 5 FTEs | \`3\_5\` |  
| 6 – 10 FTEs | \`6\_10\` |  
| 11 – 20 FTEs | \`11\_20\` |  
| More than 20 FTEs | \`over\_20\` |  
| Unknown at this stage | \`unknown\` |

\---

\#\#\# Q11 — Transport Move Volume  
\*\*Field ID:\*\* \`moves\_per\_shift\`  
\*\*Type:\*\* Single select  
\*\*Required:\*\* NO — if unanswered, no boost applied; flag for follow-up  
\*\*Note:\*\* One move \= one round trip or one-way load transfer between zones.  
Use order count, truck count, or inbound pallet volume as a proxy if a direct  
figure is unavailable.  
\*\*Question:\*\* Approximately how many internal transport moves (trips or load  
transfers) occur per shift at this site?

| Option | Value |  
|--------|-------|  
| Fewer than 20 moves per shift | \`under\_20\` |  
| 20 – 50 moves per shift | \`20\_50\` |  
| 51 – 150 moves per shift | \`51\_150\` |  
| 151 – 300 moves per shift | \`151\_300\` |  
| More than 300 moves per shift | \`over\_300\` |  
| Unknown at this stage | \`unknown\` |

\---

\#\#\# Q12 — Number of Distinct Transport Routes  
\*\*Field ID:\*\* \`route\_count\`  
\*\*Type:\*\* Single select  
\*\*Required:\*\* NO — if unanswered, default to \`unknown\`  
\*\*Note:\*\* A route is a fixed repeated path between two zones (e.g. inbound dock  
to bulk storage; bulk storage to pick face; pick face to staging). Count the  
number of such distinct recurring paths, not the number of trips per path.  
\*\*Question:\*\* How many distinct recurring internal transport routes operate  
at this site?

| Option | Value |  
|--------|-------|  
| 1 route (single fixed loop) | \`1\` |  
| 2 – 3 routes | \`2\_3\` |  
| 4 – 6 routes | \`4\_6\` |  
| More than 6 routes | \`over\_6\` |  
| Unknown at this stage | \`unknown\` |

\---

\#\# SECTION 05 — LABOUR & WORKFORCE

\#\#\# Q13 — Transport Labour Overtime  
\*\*Field ID:\*\* \`transport\_overtime\`  
\*\*Type:\*\* Single select  
\*\*Required:\*\* NO — if unanswered, no signal applied  
\*\*Note:\*\* Persistent overtime in transport roles is a direct indicator that  
permanent headcount cannot cover demand — a strong automation urgency signal.  
Answer based on job postings, worker reviews, or known operational patterns.  
\*\*Question:\*\* Is there evidence of regular or persistent overtime in internal  
transport roles at this site?

| Option | Value |  
|--------|-------|  
| No evidence of regular overtime | \`none\` |  
| Occasional overtime during peak periods only | \`seasonal\` |  
| Regular overtime most weeks (estimated \>10% of hours) | \`regular\` |  
| Heavy overtime sustained year-round (estimated \>20% of hours) | \`heavy\` |  
| Unknown at this stage | \`unknown\` |

\---

\#\#\# Q14 — Transport Role Attrition Signal  
\*\*Field ID:\*\* \`transport\_attrition\`  
\*\*Type:\*\* Single select  
\*\*Required:\*\* NO — if unanswered, no signal applied  
\*\*Note:\*\* Estimate from job posting frequency for the same roles, worker review  
recency and volume patterns, or direct knowledge. High attrition compounds  
labour cost through continuous recruitment and training overhead.  
\*\*Question:\*\* How would you characterise attrition in transport roles at this site?

| Option | Value |  
|--------|-------|  
| Low — roles appear stable, infrequent open postings | \`low\` |  
| Moderate — some turnover, recurring postings for same roles | \`moderate\` |  
| High — frequent postings, short tenure signals in reviews | \`high\` |  
| Very high — near-constant open roles, strong churn signals | \`very\_high\` |  
| Unknown at this stage | \`unknown\` |

\---

\#\# SECTION 06 — PHYSICAL INFRASTRUCTURE

\#\#\# Q15 — Ceiling / Structural Clearance  
\*\*Field ID:\*\* \`ceiling\_clearance\`  
\*\*Type:\*\* Single select  
\*\*Required:\*\* NO — if unanswered, default to \`unknown\`  
\*\*Note:\*\* Applies to the minimum clearance along the primary transport routes,  
not the highest point in the building. Relevant where tall load formats or  
mast-type tugger configurations are involved.  
\*\*Question:\*\* What is the minimum ceiling or structural clearance along  
the primary internal transport routes?

| Option | Value |  
|--------|-------|  
| Under 12 ft | \`under\_12ft\` |  
| 12 – 16 ft | \`12\_16ft\` |  
| Over 16 ft | \`over\_16ft\` |  
| Unknown at this stage | \`unknown\` |

\---

\#\#\# Q16 — Minimum Doorway / Opening Width  
\*\*Field ID:\*\* \`doorway\_width\`  
\*\*Type:\*\* Single select  
\*\*Required:\*\* NO — if unanswered, default to \`unknown\`  
\*\*Note:\*\* Applies to the narrowest doorway, fire door, or structural opening  
that the primary transport routes must pass through. Standard tugger trains  
with a loaded cart typically require 8–10 ft minimum passage width.  
\*\*Question:\*\* What is the narrowest doorway or opening along the primary  
transport routes?

| Option | Value |  
|--------|-------|  
| Under 8 ft | \`under\_8ft\` |  
| 8 – 10 ft | \`8\_10ft\` |  
| Over 10 ft | \`over\_10ft\` |  
| No restricting doorways on routes | \`unrestricted\` |  
| Unknown at this stage | \`unknown\` |

\---

\#\#\# Q17 — Site Layout  
\*\*Field ID:\*\* \`site\_layout\`  
\*\*Type:\*\* Single select  
\*\*Required:\*\* NO — if unanswered, default to \`single\_building\`  
\*\*Note:\*\* Multi-building sites with outdoor segments require weatherproofed  
vehicles or separate handoff points, which limits deployment scope and  
increases cost. This is a scope limiter, not a hard blocker.  
\*\*Question:\*\* How is the warehouse operation physically structured?

| Option | Value |  
|--------|-------|  
| Single building – all transport is internal | \`single\_building\` |  
| Multiple connected buildings – transport is under cover throughout | \`multi\_connected\` |  
| Multiple separate buildings – transport crosses outdoor areas | \`multi\_separate\` |  
| Unknown at this stage | \`unknown\` |

\---

\#\#\# Q18 — Charging Station Feasibility  
\*\*Field ID:\*\* \`charging\_feasibility\`  
\*\*Type:\*\* Single select  
\*\*Required:\*\* NO — if unanswered, default to \`unknown\`  
\*\*Note:\*\* Tugger vehicles require 240V charging points positioned near routes.  
A typical 2-shift deployment needs 2–4 charging stations. Assess availability  
of electrical capacity and floor space near the main transport loop.  
\*\*Question:\*\* Is there available space and electrical capacity near the  
primary transport routes for charging stations?

| Option | Value |  
|--------|-------|  
| Yes – space and 240V electrical capacity confirmed or likely available | \`feasible\` |  
| Partial – space available but electrical upgrade likely needed | \`partial\` |  
| Unlikely – no clear space or electrical capacity near routes | \`unlikely\` |  
| Unknown at this stage | \`unknown\` |

\---

\#\# SECTION 07 — FINANCIAL & TIMING

\#\#\# Q19 — Lease Term Remaining  
\*\*Field ID:\*\* \`lease\_remaining\`  
\*\*Type:\*\* Single select  
\*\*Required:\*\* NO — if unanswered, no timing signal applied  
\*\*Note:\*\* A site with less than 2 years remaining on its lease rarely justifies  
a capital automation investment. 3+ years is the threshold for a viable business  
case. Source from property records or company filings.  
\*\*Question:\*\* How many years remain on this facility's lease or ownership  
commitment?

| Option | Value |  
|--------|-------|  
| Less than 2 years | \`under\_2yr\` |  
| 2 – 3 years | \`2\_3yr\` |  
| 4 – 7 years | \`4\_7yr\` |  
| More than 7 years | \`over\_7yr\` |  
| Owned (no lease) | \`owned\` |  
| Unknown at this stage | \`unknown\` |

\---

\#\#\# Q20 — Capital Decision Cycle  
\*\*Field ID:\*\* \`capex\_cycle\`  
\*\*Type:\*\* Single select  
\*\*Required:\*\* NO — if unanswered, no timing signal applied  
\*\*Note:\*\* Proximity to the annual budget cycle is a timing amplifier. Source  
from fiscal year disclosures, earnings call timing, or known company patterns.  
\*\*Question:\*\* When does this company typically finalise its annual capital  
expenditure budget?

| Option | Value |  
|--------|-------|  
| Q1 (January – March) | \`q1\` |  
| Q2 (April – June) | \`q2\` |  
| Q3 (July – September) | \`q3\` |  
| Q4 (October – December) | \`q4\` |  
| Continuous / rolling budget process | \`rolling\` |  
| Unknown at this stage | \`unknown\` |

\---

\#\#\# Q21 — Competitive Automation Pressure  
\*\*Field ID:\*\* \`competitor\_automation\`  
\*\*Type:\*\* Single select  
\*\*Required:\*\* NO — if unanswered, no signal applied  
\*\*Note:\*\* Whether direct competitors operating similar facilities have deployed  
automated internal transport. Competitive parity is a timing amplifier.  
\*\*Question:\*\* Are direct competitors at similar facilities known to have  
deployed automated internal transport (AGVs, AMRs, or tugger trains)?

| Option | Value |  
|--------|-------|  
| Yes – confirmed at direct competitors | \`confirmed\` |  
| Likely – strong industry signals but not confirmed at direct competitors | \`likely\` |  
| No – not known to have automated internal transport | \`none\` |  
| Unknown at this stage | \`unknown\` |

\---

\#\#\# Q22 — Annual Transport Labour Cost (Estimate)  
\*\*Field ID:\*\* \`annual\_transport\_labour\_cost\`  
\*\*Type:\*\* Single select  
\*\*Required:\*\* NO — if unanswered, engine estimates from wage and FTE data  
\*\*Note:\*\* Fully-loaded annual cost of FTEs primarily dedicated to internal  
transport. Include wages, employer payroll taxes (\~7.65%), and benefits  
(typically 20–30% of wages). This is the primary cost-of-inaction input.  
\*\*Question:\*\* What is the estimated annual fully-loaded cost of the transport  
labour force at this site?

| Option | Value |  
|--------|-------|  
| Under $200,000 per year | \`under\_200k\` |  
| $200,000 – $500,000 per year | \`200\_500k\` |  
| $500,000 – $1,000,000 per year | \`500k\_1m\` |  
| $1,000,000 – $2,000,000 per year | \`1\_2m\` |  
| Over $2,000,000 per year | \`over\_2m\` |  
| Unknown at this stage | \`unknown\` |

\---

\#\#\# Q23 — Payback Period Expectation  
\*\*Field ID:\*\* \`payback\_expectation\`  
\*\*Type:\*\* Single select  
\*\*Required:\*\* NO — if unanswered, default to \`unknown\`  
\*\*Note:\*\* The acceptable payback period signals how the financial case needs to  
be structured and whether a standard tugger deployment ROI will clear the bar.  
Source from prior investment disclosures, management commentary, or industry  
norms for this operator type.  
\*\*Question:\*\* What payback period would this operator typically require to  
approve an automation investment of this scale?

| Option | Value |  
|--------|-------|  
| Under 12 months | \`under\_12m\` |  
| 12 – 18 months | \`12\_18m\` |  
| 18 – 36 months | \`18\_36m\` |  
| Over 36 months acceptable | \`over\_36m\` |  
| Unknown at this stage | \`unknown\` |

—

**Note: Reach out to us to customize the diagnostic even deeper. Let’s talk.**

\#\# SUMMARY

| Q | Field ID | Section | Required | Default if unanswered |  
|---|----------|---------|----------|-----------------------|  
| Q1 | \`aisle\_width\` | Physical Environment | \*\*YES\*\* | — |  
| Q2 | \`floor\_condition\` | Physical Environment | No | \`mixed\` |  
| Q3 | \`temp\_exposure\` | Physical Environment | No | \`ambient\_only\` |  
| Q4 | \`travel\_distance\` | Material Movement | \*\*YES\*\* | — |  
| Q5 | \`load\_format\` | Material Movement | No | \`pallets\` |  
| Q6 | \`load\_weight\` | Material Movement | No | \`220\_660lbs\` |  
| Q7 | \`wifi\_state\` | Infrastructure & Constraints | No | \`unknown\` |  
| Q8 | \`deployment\_constraints\` | Infrastructure & Constraints | No | \`\[\]\` |  
| Q9 | \`primary\_mhe\_type\` | Transport Operation | No | \`unknown\` |  
| Q10 | \`transport\_ftes\` | Transport Operation | No | no boost applied |  
| Q11 | \`moves\_per\_shift\` | Transport Operation | No | no boost applied |  
| Q12 | \`route\_count\` | Transport Operation | No | \`unknown\` |  
| Q13 | \`transport\_overtime\` | Labour & Workforce | No | no signal applied |  
| Q14 | \`transport\_attrition\` | Labour & Workforce | No | no signal applied |  
| Q15 | \`ceiling\_clearance\` | Physical Infrastructure | No | \`unknown\` |  
| Q16 | \`doorway\_width\` | Physical Infrastructure | No | \`unknown\` |  
| Q17 | \`site\_layout\` | Physical Infrastructure | No | \`single\_building\` |  
| Q18 | \`charging\_feasibility\` | Physical Infrastructure | No | \`unknown\` |  
| Q19 | \`lease\_remaining\` | Financial & Timing | No | no signal applied |  
| Q20 | \`capex\_cycle\` | Financial & Timing | No | no signal applied |  
| Q21 | \`competitor\_automation\` | Financial & Timing | No | no signal applied |  
| Q22 | \`annual\_transport\_labour\_cost\` | Financial & Timing | No | engine estimate |  
| Q23 | \`payback\_expectation\` | Financial & Timing | No | \`unknown\` |

\*\*Required fields:\*\* Q1 (\`aisle\_width\`), Q4 (\`travel\_distance\`)

\*\*Conservative defaults applied if unanswered:\*\*  
\- \`floor\_condition\` → \`mixed\`  
\- \`temp\_exposure\` → \`ambient\_only\`  
\- \`load\_format\` → \`pallets\`  
\- \`load\_weight\` → \`220\_660lbs\`  
\- \`wifi\_state\` → \`unknown\`  
\- \`site\_layout\` → \`single\_building\`  
\- \`deployment\_constraints\` → \`\[\]\` (empty array)

\*\*No default — field treated as absent if unanswered:\*\*  
\`transport\_ftes\`, \`moves\_per\_shift\`, \`transport\_overtime\`, \`transport\_attrition\`,  
\`lease\_remaining\`, \`capex\_cycle\`, \`competitor\_automation\`, \`annual\_transport\_labour\_cost\`,  
\`payback\_expectation\` — absent means no scoring contribution, not a conservative fallback.  
