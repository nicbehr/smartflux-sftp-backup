
import datetime
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from EC_data import EC_Data
from paths import FIGUREPATH
import pandas as pd
import matplotlib.dates as mdates
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
'''
Columns:
['Date_Time', 'DATAH_x', 'Seconds', 'Nanoseconds', 'Sequence Number',
       'Diagnostic Value', 'Diagnostic Value 2', 'CO2 Absorptance',
       'H2O Absorptance', 'CO2 (mmol/m^3)', 'CO2 (mg/m^3)', 'H2O (mmol/m^3)',
       'H2O (g/m^3)', 'Block Temperature (C)', 'Total Pressure (kPa)',
       'Box Pressure (kPa)', 'Head Pressure (kPa)', 'Aux 1 - U (m/s)',
       'Cooler Voltage (V)', 'Chopper Cooler Voltage (V)', 'Vin SmartFlux (V)',
       'CO2 (umol/mol)', 'CO2 dry(umol/mol)', 'H2O (mmol/mol)',
       'H2O dry(mmol/mol)', 'Dew Point (C)', 'Cell Temperature (C)',
       'Temperature In (C)', 'Temperature Out (C)', 'Average Signal Strength',
       'CO2 Signal Strength', 'H2O Signal Strength', 'Delta Signal Strength',
       'Flow Rate (slpm)', 'Flow Rate (lpm)', 'Flow Pressure (kPa)',
       'Flow Power (V)', 'Flow Drive (%)', 'H2O Sample', 'H2O Reference',
       'CO2 Sample', 'CO2 Reference', 'HIT Power (W)', 'Vin HIT (V)',
       'U (m/s)', 'V (m/s)', 'W (m/s)', 'T (C)', 'Anemometer Diagnostics',
       'CHK_x', 'DATAH_y', 'ALB_1_1_1(other)', 'CHK__1_1_1(other)',
       'DAQM_T_1_1_1(C)', 'DAQM_V_1_1_1(V)', 'DRM_POWER_STATUS_1_1_1(other)',
       'DRM_V_BATTERY_1_1_1(V)', 'DRM_V_MAIN_1_1_1(V)', 'LWIN_1_1_1(W/m^2)',
       'LWOUT_1_1_1(W/m^2)', 'PPFD_1_1_1(umol/m^2/s^1)', 'P_RAIN_1_1_1(mm)',
       'RH_1_1_1(%)', 'RN_1_1_1(W/m^2)', 'Relay_1_1_1(other)',
       'Relay_2_1_1(other)', 'Relay_3_1_1(other)', 'SHFSENS_1_1_1(other)',
       'SHFSENS_2_1_1(other)', 'SHFSENS_3_1_1(other)', 'SHF_1_1_1(W/m^2)',
       'SHF_2_1_1(W/m^2)', 'SHF_3_1_1(W/m^2)', 'SWC_1_1_1(m^3/m^3)',
       'SWC_2_1_1(m^3/m^3)', 'SWC_3_1_1(m^3/m^3)', 'SWIN_1_1_1(W/m^2)',
       'SWOUT_1_1_1(W/m^2)', 'TA_1_1_1(C)', 'TCNR4_C_1_1_1(C)', 'TS_1_1_1(C)',
       'TS_2_1_1(C)', 'TS_3_1_1(C)', 'TS_4_1_1(C)', 'TS_5_1_1(C)',
       'TS_6_1_1(C)', 'CHK_y']
'''

monthyearFmt = mdates.DateFormatter('%y-%m-%d %H')

def flowdrive_plot(ec_data:EC_Data):
    fig = plt.figure()
    plt.plot(ec_data.data.index, ec_data.data["Flow Drive (%)"])
    ax = fig.gca()
    ax.xaxis.set_major_formatter(monthyearFmt)
    plt.xticks(rotation=60)
    plt.xlabel("Time [Y-M-D H]")
    plt.ylabel("Flowdrive [%]")
    plt.tight_layout()
    return fig
    
def flowrate_plot(ec_data:EC_Data):
    fig = plt.figure()
    plt.plot(ec_data.data.index, ec_data.data["Flow Rate (lpm)"])
    ax = fig.gca()
    ax.xaxis.set_major_formatter(monthyearFmt)
    plt.xticks(rotation=60)
    plt.xlabel("Time [Y-M-D H]")
    plt.ylabel("Flow Rate (lpm)")
    plt.tight_layout()
    return fig

def sonic_t(ec_data:EC_Data):
    fig = plt.figure()
    plt.plot(ec_data.data.index, ec_data.data["T (C)"])
    ax = fig.gca()
    ax.xaxis.set_major_formatter(monthyearFmt)
    plt.xticks(rotation=60)
    plt.xlabel("Time [Y-M-D H]")
    plt.ylabel("Sonic T [°C]")
    plt.tight_layout()
    return fig

def CO2_Signal_Strength_plot(ec_data:EC_Data):
    fig = plt.figure()
    plt.plot(ec_data.data.index, ec_data.data["CO2 Signal Strength"])
    ax = fig.gca()
    y_formatter = ScalarFormatter(useOffset=False)
    ax.yaxis.set_major_formatter(y_formatter)    
    ax.xaxis.set_major_formatter(monthyearFmt)
    plt.xticks(rotation=60)
    plt.xlabel("Time [Y-M-D H]")
    plt.ylabel("CO2 Signal Strength [%]")
    plt.tight_layout()
    return fig

    
def H2O_Signal_Strength_plot(ec_data:EC_Data):
    fig = plt.figure()
    plt.plot(ec_data.data.index, ec_data.data["H2O Signal Strength"])
    ax = fig.gca()
    ax.xaxis.set_major_formatter(monthyearFmt)
    plt.xticks(rotation=60)
    plt.xlabel("Time [Y-M-D H]")
    plt.ylabel("H2O Signal Strength [%]")
    plt.tight_layout()
    return fig

def make_files_plot(df:pd.DataFrame):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    cax = ax.pcolor(df, edgecolors='gray', linewidths=.5)
    plt.title("File sizes of the last 30 days [kb]")
    cb_formatter = ScalarFormatter().set_scientific(False)
    fig.colorbar(cax, format=cb_formatter)
    ax.set_xticks(np.arange(31))
    ax.set_xticklabels(df.columns)
    ax.set_yticks(np.arange(0,len(df.index)))
    ax.set_yticklabels(df.index)
 
    for label in ax.yaxis.get_ticklabels()[::2]:
        label.set_visible(False)    
    plt.xticks(rotation=90)
    plt.tight_layout()

    fig.savefig(FIGUREPATH+"/files.png")
    return fig

def make_plot_pdf(ec_data:EC_Data, df):
    plot1 = flowdrive_plot(ec_data)
    plot2 = flowrate_plot(ec_data)
    plot3 = sonic_t(ec_data)
    plot4 = CO2_Signal_Strength_plot(ec_data)
    plot5 = H2O_Signal_Strength_plot(ec_data)
    plot6 = make_files_plot(df)
    now = datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S")

    pp = PdfPages(FIGUREPATH+'/backupfigures_'+str(now)+'.pdf')
    pp.savefig(plot1)
    pp.savefig(plot2)
    pp.savefig(plot3)
    pp.savefig(plot4)
    pp.savefig(plot5)
    pp.savefig(plot6)
    pp.close()