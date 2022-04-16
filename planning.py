#!/usr/bin/python3
# coding: utf-8
"""
this is planning.py
"""


class Planning():
    "planning class made of static methods for gis calculus"

    @staticmethod
    def isdigitpoint(arg):
        "return 1 if arg is - or digit or ."
        digitspoint = {
            "-", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."
        }
        for i in digitspoint:
            if str(arg) == str(i):
                return 1
        return 0

    @staticmethod
    def deccoord(chaine):
        "renvoie les points floatwkt"  # [[x1,y1],[x2,y2]...]
        listepoints = []
        doubletpoints = []
        points = ""
        doublet = 0
        index2 = 1
        for index1 in range(len(chaine)):
            if Planning.isdigitpoint(chaine[index1]):
                points += chaine[index1]
            if (Planning.isdigitpoint(chaine[index2]) == 0
                    and Planning.isdigitpoint(chaine[index1]) == 1):
                doubletpoints.append(float(points))
                doublet += 1
                points = ""
                if doublet == 2:
                    listepoints.append(tuple(doubletpoints))
                    doubletpoints = []
                    doublet = 0
            if index2 != len(chaine) - 1:
                index2 += +1
        return tuple(listepoints)

    @staticmethod
    def valeursabs(arg):
        "return absolute value of arg"
        if arg < 0:
            return -arg
        if arg >= 0:
            return +arg

    @staticmethod
    def distancepoint(pointsxy):
        "distance euclidienne,le systeme de coordonnees nest pas precise"
        if (Planning.valeursabs(pointsxy[0][0] - pointsxy[1][0]) < 100000 and
                Planning.valeursabs(pointsxy[0][1] - pointsxy[1][1]) < 100000):
            dist = ((pointsxy[1][1] - pointsxy[0][1])**2 +
                    (pointsxy[1][0] - pointsxy[0][0])**2)**(1 / 2)
        else:
            dist = 666666
        return dist

    @staticmethod
    def centroide(geompolygone):
        "return centroid of polygon geompolygone which is a list of points"
        sigmax = 0
        sigmay = 0
        for i in geompolygone:
            sigmax += i[0]
            sigmay += i[1]
        resultx = sigmax / (len(geompolygone))
        resulty = sigmay / (len(geompolygone))
        return (resultx, resulty)

    @staticmethod
    def surf(triangle):
        "methode surf triangle par determinant matriciel"
        # liste [[x1,y1],[x2,y2],[x3,y3]]
        # det:1/2[x1(y2–y3)+x2(y3–y1)+x3(y1–y2)]
        surf = (1 / 2) * (triangle[0][0] *
                          (triangle[1][1] - triangle[2][1]) + triangle[1][0] *
                          (triangle[2][1] - triangle[0][1]) + triangle[2][0] *
                          (triangle[0][1] - triangle[1][1]))
        return Planning.valeursabs(surf)

    @staticmethod
    def dedans(point, listetriangle):
        "1 si point dans 1 triangle de listetriangle"
        for triangle in listetriangle:
            surf = Planning.surf(triangle)
            surf1 = Planning.surf([point, triangle[0], triangle[1]])
            surf2 = Planning.surf([point, triangle[0], triangle[2]])
            surf3 = Planning.surf([point, triangle[1], triangle[2]])
            if surf1 + surf2 + surf3 - surf < 0.001:
                return 1

    @staticmethod
    def indexdist(point, listpoint):
        "ordonne la liste des points listepointt selon la distance à pointt"
        result0 = []
        result = []
        for pointi in listpoint:
            result0.append([pointi, Planning.distancepoint([pointi, point])])
        result0.sort(key=lambda x: x[1])
        for pointk in result0:
            result.append(pointk[0])
        return result

    @staticmethod
    def fonction(polygon):
        "return surface of polygon=[pt1,pt2,...,ptn]"
        surf = 0
        list_triangle = []  # listedetriangles
        listpoint = []  # listedepoints
        xxyy = []  # [[xmin,xmax],[ymin,ymax]]
        triangle = []  # triangle
        for i in range(len(polygon)):
            if i < 3:
                triangle.append(polygon[i])  # i<3
                listpoint.append(polygon[i])
                if i == 2:
                    list_triangle.append(triangle)
                    xxyy = Planning.minmaxt(list_triangle)
            # condition sur i>=3
            else:
                # verifier l[i] hors des polygones
                boolean = 1
                if (polygon[i][0] - xxyy[0][0] >= 0
                        and polygon[i][0] - xxyy[0][1] <= 0
                        and polygon[i][1] - xxyy[1][0] >= 0
                        and polygon[i][1] - xxyy[1][1] <= 0):
                    # hors xminxmaxyminymax:out dans xminxmax hors yminymax:out hors xminxmax dans yminymax:out
                    # dans xminxmax dans yminymax surf sommedestriangles=surftriangleprecedent->in surf sommedestriangles>surftriangleprecedent->out
                    if Planning.dedans(
                            polygon[i], list_triangle
                    ):  # dedans(pt,listetriangle) renvoie 1 si à l'interieur d'un des triangle
                        boolean = 0
                else:
                    pass

                if boolean != 0:
                    # creertriangle_pt1
                    triangle = [polygon[i]]
                    pt1 = Planning.indexdist(
                        polygon[i], listpoint
                    )  # liste des points triés selon distance à l[i]
                    ###ici le index gist en postgis accelererait probablement
                    triangle.append(pt1[0])

                    # creertriangle_pt2
                    for k in range(1, len(pt1)):
                        if Planning.secantlll(
                            [polygon[i], pt1[k]], pt1, k
                        ):  # si la ligne l[i]pt1[k] interesecte une des lignes pt1[0]autresptsdept1
                            pass
                        else:
                            triangle.append(pt1[k])
                            # print(t)
                            list_triangle.append(triangle)
                            xxyy = Planning.minmaxt(list_triangle)
                            listpoint.append(polygon[i])
                            break
        for j in list_triangle:
            surf += Planning.surf(j)
        return surf

    @staticmethod
    def minmaxt(list_triangle):
        "renvoie les xxyy=[]#[[xmin,xmax],[ymin,ymax]] de la liste de triangle"
        listx = []
        listy = []
        for i in list_triangle:
            listx.append(i[0][0])
            listx.append(i[1][0])
            listx.append(i[2][0])
            listy.append(i[0][1])
            listy.append(i[1][1])
            listy.append(i[2][1])
        xmin = min(listx)
        xmax = max(listx)
        ymin = min(listy)
        ymax = max(listy)
        return [[xmin, xmax], [ymin, ymax]]

    @staticmethod
    def secantlll(xy1, lpt, k):
        "renvoie 1 si xy1 et les lignes de lpt sont secantes sauf la kieme"
        for i in range(1, len(lpt)):
            if i == k:
                pass
            if Planning.secant(xy1, [lpt[0], lpt[i]]):
                return 1

    @staticmethod
    def secant(xy1, xy2):
        "return 1 si xy1 et xy2 sont secants par determinant matriciel"
        # xy[[x1,y1],[x'1,y'1]]
        # si colinéaire det=0
        x1min = min(xy1[0][0], xy1[1][0])
        x1max = max(xy1[0][0], xy1[1][0])
        y1min = min(xy1[0][1], xy1[1][1])
        y1max = max(xy1[0][1], xy1[1][1])
        x2min = min(xy2[0][0], xy2[1][0])
        x2max = max(xy2[0][0], xy2[1][0])
        y2min = min(xy2[0][1], xy2[1][1])
        y2max = max(xy2[0][1], xy2[1][1])
        xmax = max(x1max, x2max)
        xmin = min(x1min, x2min)
        if (Planning.valeursabs((xy1[1][0] - xy1[0][0]) *
                                (xy2[1][1] - xy2[0][1]) -
                                (xy1[1][1] - xy1[0][1]) *
                                (xy2[1][0] - xy2[0][0])) == 0
            ):  ##etonnant, pas ==0 sur un cas a1=a2
            return 0
        if ((x1max < x2min) or
            (x1min > x2max)) and ((y1max < y2min) or
                                  (y1min > y2max)):  # condition sur disjoints
            return 0
        else:  # equations ax+b
            if (xy1[1][0] - xy1[0][0]) == 0:
                a2 = (xy2[1][1] - xy2[0][1]) / (xy2[1][0] - xy2[0][0])
                b2 = xy2[1][1] - a2 * (xy2[1][0])
                y2 = a2 * xy1[1][0] + b2
                if y2 <= y1max and y2 >= y1min:
                    return 1
                else:
                    return 0
            elif (xy2[1][0] - xy2[0][0]) == 0:
                a1 = (xy1[1][1] - xy1[0][1]) / (xy1[1][0] - xy1[0][0])
                b1 = xy1[1][1] - a1 * (xy1[1][0])
                y1 = a1 * xy2[1][0] + b1
                if y1 <= y2max and y1 >= y2min:
                    return 1
                else:
                    return 0
            else:
                a1 = (xy1[1][1] - xy1[0][1]) / (xy1[1][0] - xy1[0][0])
                b1 = xy1[1][1] - a1 * (xy1[1][0])
                a2 = (xy2[1][1] - xy2[0][1]) / (xy2[1][0] - xy2[0][0])
                b2 = xy2[1][1] - a2 * (xy2[1][0])
                if ((b2 - b1) / (a1 - a2)) <= xmax and ((b2 - b1) /
                                                        (a1 - a2)) >= xmin:
                    return 1
