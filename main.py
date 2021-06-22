import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import os
import datetime

cwd = os.getcwd()

## Globally used series of which rows had patients showing up
showSeries = pd.Series()
## Globally used series of which rows had patients did not show up
noShowSeries = pd.Series()

##
# @brief Function used to plot analysis
# @param showData   - Array of panda.series data where the patient showed up
# @param noShowData - Array of panda.series data where the patient didn't show up
# @param labels     - Array of labels for graph
# @param title      - Title of figure
def PlotAnalysis(showData, noShowData, labels, title):
    if len(showData) != len(noShowData) and len(showData) != len(labels):
        return
        
    # 2 Axes for show/noShow
    fig, (showAxes, noShowAxes) = plt.subplots(nrows = 1, ncols = 2)
    figureSize = (12,8)

    fig.suptitle(title)

    showAxes.set_title('Show')

    showTotal = 0
    noShowTotal = 0

    for i in range(len(showData)):
        showData[i].plot(ax=showAxes, kind='hist', label=labels[i], legend=True, figsize=figureSize)
        showTotal = showTotal + showData[i].size

    # Label the bars with the frequency of that value as well as percentage
    for i in range(len(showData)):
        showAxes.annotate("{}({:.3f}%)".format(showData[i].size, (showData[i].size / showTotal) * 100.0), xy=(showData[i].iloc[0], showData[i].size), xycoords="data")

    noShowAxes.set_title('NoShow')

    for i in range(len(noShowData)):
        noShowData[i].plot(ax=noShowAxes, kind='hist', label=labels[i], legend=True, figsize=figureSize)
        noShowTotal = noShowTotal + noShowData[i].size

    # Label the bars with the frequency of that value as well as percentage
    for i in range(len(noShowData)):
        noShowAxes.annotate("{}({:.3f}%)".format(noShowData[i].size, (noShowData[i].size / noShowTotal) * 100.0), xy=(noShowData[i].iloc[0], noShowData[i].size), xycoords="data")

    if not os.path.exists('Plots'):
        os.mkdir('Plots')
    plt.savefig('Plots/' + title + 'Analysis.png', facecolor='white')

## Function to analyze the Appointment Data
# @param appointmentDayData   - panda.series appointment day data
def AnalyzeAppointmentDay(appointmentDayData):
    print("Analyzing Appointment Day")
    global showSeries, noShowSeries

    weeknumber = np.array([])

    # Get which day of the week each appointment is at
    for data in appointmentDayData:
        weeknumber = np.append(weeknumber, data.weekday())

    fig, (showAxes, noShowAxes) = plt.subplots(nrows = 1, ncols = 2, figsize=(10, 8))

    fig.suptitle('AppointmentDay')
    matplotlib.pyplot.subplots_adjust(wspace = 0.8)

    show_weeknoSeries = pd.Series(weeknumber[showSeries])
    noShow_weeknoSeries = pd.Series(weeknumber[noShowSeries])

    # Get counts of each week number and normalize to [0.0, 1.0)
    chart_values = show_weeknoSeries.value_counts(normalize=True)

    # Convert values to percent scaling
    chart_values = chart_values.apply(lambda x : x * 100)

    # Sort by index for labels to match up
    chart_values.sort_index(ascending=True, inplace=True)
    showAxes.set_title('Show')
    showAxes.pie(chart_values, labels=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'], autopct='%1.1f%%',
        shadow=True, startangle=90, radius=10.0)
    showAxes.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    # Get counts of each week number and normalize to [0.0, 1.0)
    chart_values = noShow_weeknoSeries.value_counts(normalize=True)
    
    # Convert values to percent scaling
    chart_values = chart_values.apply(lambda x : x * 100)

    # Sort by index for labels to match up
    chart_values.sort_index(ascending=True, inplace=True)
    noShowAxes.set_title('NoShow')
    noShowAxes.pie(chart_values, labels=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'], autopct='%1.1f%%',
        shadow=True, startangle=90, radius=10.0)
    noShowAxes.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.savefig('Plots/AppointmentDayAnalysis.png', facecolor='white')

## Function to analyze the Hypertension data
# @param hypertensionData   - panda.series hypertension data
def AnalyzeHyperTension(hypertensionData):
    print("Analyzing Hyperternsion")
    global showSeries, noShowSeries

    # Get which rows had patient showing up
    showed_hypertensionData = hypertensionData[showSeries]

    # Get which rows the patient didn't show up
    noShow_hypertensionData = hypertensionData[noShowSeries]

    showed_hasHypertension = showed_hypertensionData == 1.0
    showed_noHypertension = showed_hypertensionData == 0.0
    noShow_hasHypertension = noShow_hypertensionData == 1.0
    noShow_noHypertension = noShow_hypertensionData == 0.0

    PlotAnalysis(showData=[showed_hypertensionData[showed_hasHypertension], showed_hypertensionData[showed_noHypertension]],
                    noShowData=[noShow_hypertensionData[noShow_hasHypertension], noShow_hypertensionData[noShow_noHypertension]],
                    labels=['HasHypertension', 'NoHypertension'],
                    title='Hypertension'
    )

## Function to analyze the Diabetes data
# @param diabetesData   - panda.series Diabetes data
def AnalyzeDiabetes(diabetesData):
    print("Analyzing Diabetes")
    global showSeries, noShowSeries

    # Get which rows had patient showing up
    showed_diabetesData = diabetesData[showSeries]

    # Get which rows the patient didn't show up
    noShow_diabetesData = diabetesData[noShowSeries]

    showed_hasDiabetes = showed_diabetesData == 1.0
    showed_noDiabetes = showed_diabetesData == 0.0
    noShow_hasDiabetes = noShow_diabetesData == 1.0
    noShow_noDiabetes = noShow_diabetesData == 0.0

    PlotAnalysis(showData=[showed_diabetesData[showed_hasDiabetes], showed_diabetesData[showed_noDiabetes]],
                noShowData=[noShow_diabetesData[noShow_hasDiabetes], noShow_diabetesData[noShow_noDiabetes]],
                labels=['HasDiabetes', 'NoDiabetes'],
                title='Diabetes'
    )

## Function to analyze the alcoholism data
# @param alcoholismData   - panda.series alcoholism data
def AnalyzeAlcoholism(alcoholismData):
    print("Analyzing Alcoholism")
    global showSeries, noShowSeries

    # Get which rows had patient showing up
    showed_alcoholismData = alcoholismData[showSeries]

    # Get which rows the patient didn't show up
    noShow_alcoholismData = alcoholismData[noShowSeries]

    showed_hasAlcoholism = showed_alcoholismData == 1.0
    showed_noAlcoholism = showed_alcoholismData == 0.0
    noShow_hasAlcoholism = noShow_alcoholismData == 1.0
    noShow_noAlcoholism = noShow_alcoholismData == 0.0

    PlotAnalysis(showData=[showed_alcoholismData[showed_hasAlcoholism], showed_alcoholismData[showed_noAlcoholism]],
                noShowData=[noShow_alcoholismData[noShow_hasAlcoholism], noShow_alcoholismData[noShow_noAlcoholism]],
                labels=['HasAlcoholism', 'NoAlcoholism'],
                title='Alcoholism'
    )

## Function to analyze the Handicap data
# @param handicapData   - panda.series Handicap data
def AnalyzeHandicap(handicapData):
    print("Analyzing Handicap")
    global showSeries, noShowSeries

    # Get which rows had patient showing up
    showed_handicapData = handicapData[showSeries]

    # Get which rows the patient didn't show up
    noShow_handicapData = handicapData[noShowSeries]

    showed_hasHandicap = showed_handicapData == 1.0
    showed_noHandicap = showed_handicapData == 0.0
    noShow_hasHandicap = noShow_handicapData == 1.0
    noShow_noHandicap = noShow_handicapData == 0.0

    PlotAnalysis(showData=[showed_handicapData[showed_hasHandicap], showed_handicapData[showed_noHandicap]],
                noShowData=[noShow_handicapData[noShow_hasHandicap], noShow_handicapData[noShow_noHandicap]],
                labels=['HasHandicap', 'NoHandicap'],
                title='Handicap'
    )

## Function to analyze the SMS Received data
# @param smsData   - panda.series SMS Received data
def AnalyzeSMSReceive(smsData):
    print("Analyzing SMS Received")
    global showSeries, noShowSeries

    # Get which rows had patient showing up
    showed_smsData= smsData[showSeries]

    # Get which rows the patient didn't show up
    noShow_smsData = smsData[noShowSeries]

    showed_rcvedSMSData = showed_smsData == 1
    showed_noRcvSMSData = showed_smsData == 0
    noShow_rcvedSMSData = noShow_smsData == 1
    noShow_noRcvSMSData = noShow_smsData == 0

    PlotAnalysis(showData=[showed_smsData[showed_rcvedSMSData], showed_smsData[showed_noRcvSMSData]],
            noShowData=[noShow_smsData[noShow_rcvedSMSData], noShow_smsData[noShow_noRcvSMSData]],
            labels=['ReceivedSMS', 'NotReceivedSMS'],
            title='SMS'
    )

def Dimension1Analysis(df, xCol, color):
    plt.figure(figsize = (12,8))
    sns.countplot(data=df, x=xCol, color=color)
    plt.savefig('Plots/' + xCol + '1DAnalysis.png', facecolor='white')

def main():
    global showSeries, noShowSeries
    csvFile = os.path.join(cwd, "noshowappointments-kagglev2-may-2016.csv")
    df = pd.read_csv(csvFile)
    df.info()
    
    print("Number of duplicated rows: {}".format(df.duplicated().sum()))
    df.rename(columns={"Hipertension":"Hypertension", "Handcap":"Handicap", "No-show":"NoShow", "Neighbourhood": "Neighborhood"}, inplace=True)

    # Columns that shouldn't affect whether the patient shows up or not
    df.drop(['PatientId', 'AppointmentID', 'ScheduledDay', 'Age', 'Gender', 'Scholarship', 'Neighborhood'], axis=1, inplace=True)
    showSeries = pd.Series(data = df.NoShow == 'No')
    noShowSeries = pd.Series(data = df.NoShow == 'Yes')

    # Clean to datetime values
    df['AppointmentDay'] = pd.to_datetime(df['AppointmentDay'])

    # Analyze data now
    Dimension1Analysis(df, "Alcoholism", "steelblue")
    AnalyzeAlcoholism(df.Alcoholism)
    AnalyzeAppointmentDay(df.AppointmentDay)
    Dimension1Analysis(df, "Diabetes", "steelblue")
    AnalyzeDiabetes(df.Diabetes)
    Dimension1Analysis(df, "Handicap", "steelblue")
    AnalyzeHandicap(df.Handicap)
    Dimension1Analysis(df, "Hypertension", "steelblue")
    AnalyzeHyperTension(df.Hypertension)
    Dimension1Analysis(df, "SMS_received", "steelblue")
    AnalyzeSMSReceive(df.SMS_received)
    

if __name__ == "__main__":
    main()