from flask import Flask, render_template
import csv

app = Flask(__name__)


house_aRangement = [[1,0,"2A"],[0,1,"1A"],[1,1,"1B"],[2,1,"2B"],[3,1,"6A"],[4,1,"6B"],[5,1,"3B"],[6,1,"3A"],[0,2,"4A"],[1,2,"4B"],[2,2,"5A"],[3,2,"5B"],[4,2,"7B"],[5,2,"7A"],[0,3,"8A"],[1,3,"8B"],[2,3,"10A"],[3,3,"10B"],[4,3,"11A"],[10,3,"30A"],[11,3,"30B"],[12,3,"35A"],[13,3,"35B"],[14,3,"31B"],[15,3,"32B"],[0,4,"12A"],[1,4,"9A"],[2,4,"9B"],[3,4,"15B"],[4,4,"11B"],[9,4,"34A"],[10,4,"36A"],[11,4,"36B"],[12,4,"37A"],[13,4,"37B"],[14,4,"38A"],[15,4,"38B"],[16,4,"39A"],[0,5,"12B"],[1,5,"13A"],[2,5,"13B"],[3,5,"15A"],[4,5,"32A"],[9,5,"34B"],[10,5,"40A"],[11,5,"40B"],[12,5,"41A"],[13,5,"41B"],[14,5,"42A"],[15,5,"42B"],[16,5,"43A"],[0,6,"17A"],[1,6,"17B"],[2,6,"14A"],[3,6,"14B"],[4,6,"31A"],[8,6,"44A"],[9,6,"45A"],[10,6,"45B"],[11,6,"59A"],[12,6,"60A"],[13,6,"66A"],[14,6,"66B"],[15,6,"67A"],[16,6,"43B"],[17,6,"39B"],[0,7,"16A"],[1,7,"18A"],[2,7,"29A"],[3,7,"29B"],[9,7,"44B"],[10,7,"46A"],[11,7,"59B"],[12,7,"60B"],[13,7,"64A"],[14,7,"65A"],[15,7,"67B"],[16,7,"53A"],[0,8,"16B"],[1,8,"18B"],[2,8,"47A"],[3,8,"33A"],[9,8,"33B"],[10,8,"46B"],[11,8,"61A"],[12,8,"62A"],[13,8,"63A"],[14,8,"65B"],[15,8,"53B"],[16,8,"54B"],[0,9,"19A"],[1,9,"20A"],[2,9,"20B"],[3,9,"58B"],[4,9,"21A"],[5,9,"21B"],[9,9,"48A"],[10,9,"49A"],[11,9,"61B"],[12,9,"62B"],[13,9,"63B"],[14,9,"64B"],[15,9,"52A"],[16,9,"54A"],[0,10,"22B"],[1,10,"19B"],[2,10,"23B"],[3,10,"25B"],[4,10,"24B"],[5,10,"25A"],[6,10,"28A"],[9,10,"47B"],[10,10,"48B"],[11,10,"49B"],[12,10,"50A"],[13,10,"50B"],[14,10,"51A"],[15,10,"51B"],[16,10,"52B"],[0,11,"22A"],[1,11,"23A"],[2,11,"24A"],[3,11,"26B"],[4,11,"26A"],[5,11,"27A"],[6,11,"27B"],[7,11,"28B"],[10,11,"55A"],[11,11,"55B"],[12,11,"56A"],[13,11,"56B"],[14,11,"58A"],[15,11,"57A"],[16,11,"57B"]]
senate_aRangement = [[1,0,"2"],[0,1,"1"],[1,1,"4"],[2,1,"5"],[3,1,"6"],[4,1,"3"],[0,2,"8"],[1,2,"9"],[2,2,"10"],[3,2,"11"],[4,2,"7"],[8,2,"35"],[0,3,"12"],[1,3,"13"],[2,3,"14"],[3,3,"15"],[4,3,"32"],[7,3,"34"],[8,3,"36"],[9,3,"37"],[10,3,"38"],[0,4,"16"],[1,4,"29"],[2,4,"30"],[3,4,"31"],[6,4,"33"],[7,4,"40"],[8,4,"41"],[9,4,"42"],[10,4,"39"],[11,4,"43"],[0,5,"17"],[1,5,"18"],[2,5,"47"],[3,5,"58"],[6,5,"48"],[7,5,"44"],[8,5,"46"],[9,5,"45"],[10,5,"59"],[11,5,"60"],[12,5,"66"],[0,6,"19"],[1,6,"20"],[2,6,"21"],[6,6,"50"],[7,6,"49"],[8,6,"61"],[9,6,"62"],[10,6,"63"],[11,6,"64"],[0,7,"24"],[1,7,"25"],[2,7,"26"],[6,7,"51"],[7,7,"52"],[8,7,"65"],[9,7,"67"],[10,7,"53"],[11,7,"54"],[0,8,"22"],[1,8,"23"],[2,8,"27"],[3,8,"28"],[7,8,"55"],[8,8,"57"],[9,8,"56"]]

#build dict of campaign finance data for later use
with open('data/sep-16-mnleg-ies.csv','r') as f:
    reader = csv.DictReader(f)
    camfi_data = {}
    for row in reader:
        district = row['district']
        party = row['party']
        total = row['total']

        if district in camfi_data:
            camfi_data[district][party] = total
        else:
            camfi_data[district] = {party: total}

def get_spending(chamber, party):
    #calculate classes based on equal-interval quintiles
    amts_raised = []
    if chamber == "house": #house district
        for district in camfi_data:
            if district[-1] in ["A","B"]:
                amts_raised.append(float(camfi_data.get(district,{}).get(party,0)))
    else: #senate district
        for district in camfi_data:
            if district[-1] not in ["A","B"]:
                amts_raised.append(float(camfi_data.get(district,{}).get(party,0)))
    return amts_raised


def assign_classes(name, party):
    #This is always going to need to be customized according to the project
    classes = []
    chamber = "senate"
    if name[-1] in ["A", "B"]:
        chamber = "house"
    amts_raised = get_spending(chamber, party)

    fifth = max(amts_raised)/5
    this_total = float(camfi_data.get(name,{}).get(party,0))
    if this_total == 0:
        classes.append("no-data")
    else:
        if this_total < fifth:
            classes.append("q1")
        elif this_total < fifth*2:
            classes.append("q2")
        elif this_total < fifth*3:
            classes.append("q3")
        elif this_total < fifth*4:
            classes.append("q4")
        elif this_total > fifth*4:
            classes.append("q5")

    return classes #list of classes

def get_legend(chamber,party):
    amts_raised = get_spending(chamber, party)
    top = max(amts_raised)

    return [
                {
                    'class': 'q5',
                    'text': 'Up to ${:,}'.format(int(top))
                },
                {
                    'class': 'q4',
                    'text': 'Up to ${:,}'.format(int(top*.8))
                },
                {
                    'class': 'q3',
                    'text': 'Up to ${:,}'.format(int(top*.6))
                },
                {
                    'class': 'q2',
                    'text': 'Up to ${:,}'.format(int(top*.4))
                },
                {
                    'class': 'q1',
                    'text': 'Up to ${:,}'.format(int(top*.2))
                },
                {
                    'class': 'no-data',
                    'text': 'No spending data reported'
                }
           ]

def total_rows(arangement):
    return max([el[1] for el in arangement])

def total_cols(arangement):
    return max([el[0] for el in arangement])

def aranged_data(arangement, party):
    #build a list of rows containing a list of cells ordered by column
    rows = []
    for r in range(total_rows(arangement)+1):
        cells = []
        for c in range(total_cols(arangement)+1):
            inserted = False
            for el in arangement:
                if c == el[0] and r == el[1]:
                    name = el[2]
                    total = round((float(camfi_data.get(name,{}).get(party,0))),2)
                    if total == 0:
                        total = 'No spending data reported'
                    else:
                        total = '${:,}'.format(total)
                    cells.append({'name':name,
                                  'classes': assign_classes(name, party),
                                  'total': total
                                  })
                    inserted = True
            if not inserted:
                cells.append({'name':""})
        rows.append(cells)
    return rows

@app.route("/")
def home():

    data = [
                {
                 "title": "Minnesota House — Spending by Republican-aligned groups",
                 "chamber": "House",
                 "carto": aranged_data(house_aRangement, "R"),
                 "legend": get_legend("house", "R")
                },

                {
                 "title": "Minnesota House — Spending by Democrat-aligned groups",
                 "chamber": "House",
                 "carto": aranged_data(house_aRangement, "D"),
                 "legend": get_legend("house", "D")
                },

                {
                 "title": "Minnesota Senate — Spending by Republican-aligned groups",
                 "chamber": "Senate",
                 "carto": aranged_data(senate_aRangement, "R"),
                 "legend": get_legend("senate", "R")
                },

                {
                 "title": "Minnesota Senate — Spending by Democrat-aligned groups",
                 "chamber": "Senate",
                 "carto": aranged_data(senate_aRangement, "D"),
                 "legend": get_legend("senate", "D")
                }
           ]

    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
