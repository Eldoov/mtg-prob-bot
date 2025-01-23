import math
from Algorithm import factCalc, getCombos


def initiateDate(deckInfo, sampleInfo):
    """
    :param deckInfo: input deck info (a,b,c,d,...)
    :param sampleInfo: input desired pop info (a1, b1, c1, d1,...)
    :return: probability of drawing certain desired cards
    """
    totalCards = deckInfo.pop(0)  # a
    totalDrawCards = sampleInfo.pop(0)  # a1
    remainingCardsInDeck = totalCards - sum(deckInfo)  # n
    remainingSample = totalDrawCards - sum(sampleInfo)  # n1
    length = len(sampleInfo)
    return totalCards, totalDrawCards, remainingCardsInDeck, remainingSample, length


def getSingleProb(totalCards, totalDrawCards, remainingCardsInDeck,
                  remainingSample, length, deckInfo, sampleInfo):
    N = 0

    # initiating
    lstRes = [0] * length  # factorial results between two inputs = x! / x1!(x-x1)!
    Total = int(factCalc(totalCards, totalDrawCards))  # a! / a1!(a-a1)!

    for i in range(len(lstRes)):
        if sampleInfo[i] <= deckInfo[i]:
            lstRes[i] = int(factCalc(deckInfo[i], sampleInfo[i]))

    lstProd = math.prod(lstRes)  # products of factorial results

    if remainingSample > 0 and remainingCardsInDeck > 0:
        N = factCalc(remainingCardsInDeck, remainingSample)

    if N > 0:
        comb = int(lstProd * N)
    else:
        comb = int(lstProd)

    val = comb / Total
    return val, comb, Total


def getAllProb(deckInfo, sampleInfo):
    (totalCards, totalDrawCards, remainingCardsInDeck,
     remainingSample, length) = initiateDate(deckInfo, sampleInfo)
    totalProb = 0
    botMsg = []
    message_text = ""

    if remainingCardsInDeck < 0 or  remainingSample < 0:
        errorStr = "NO, STAHP~~~~~"
        return errorStr

    if remainingCardsInDeck > 0 and remainingSample > 0:
        deckInfo.append(remainingCardsInDeck)
        sampleInfo.append(0)
        remainingCardsInDeck = 0
        length += 1

    if remainingSample > 0:
        all_combos = getCombos(totalDrawCards, sampleInfo)
        for combo in all_combos:
            prob, comb, Total = getSingleProb(totalCards, totalDrawCards, remainingCardsInDeck,
                                 remainingSample, length, deckInfo, combo)
            totalProb = totalProb + prob
            probInWords = f"{prob:.4%}"
            if prob > 0:
                message_text = " ".join(map(str, ("When", combo, "Prob is ", comb, "/", Total, "=", probInWords)))
                botMsg.append(message_text)

    else:
        prob, comb, Total = getSingleProb(totalCards, totalDrawCards, remainingCardsInDeck,
                                          remainingSample, length, deckInfo, sampleInfo)
        print("the prob is ", comb, "/", Total, "=", prob)
    botMsg.append(f"The total prob for all is {totalProb:.5%}")
    final_output = "\n".join(botMsg)
    simpRes = f"{totalProb:.4%}"
    return final_output, simpRes


#getAllProb([99, 40, 15, 10, 34], [7, 3, 0, 0,0])
#getAllProb([99, 40, 15, 10], [7, 3, 0, 0])
