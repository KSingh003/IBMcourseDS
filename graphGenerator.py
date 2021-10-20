#
#Program Name:        graphGenerator.py
#Last Modified:       July 20, 2020
#Program Description: Generates graphs based on the statistical
#                     data generated from Oboe. Creates graphs
#                     for bitrate quality, buffering time,
#                     bitrate changes and overall QoE.
#

import copy

import numpy as np
import matplotlib.pyplot as plt

LINE_COLOR = "#454545FF"

LINE_8_COLOR = "#00C2D1FF"
LINE_16_COLOR = "#00727AFF"
LINE_32_COLOR = "#002629FF"

#Toggle this to set live or recorded data
IS_LIVE = True

STREAMING_SECONDS = 60

#Change this for current working directory
BASE_FILE_PATH = "/home/stu15/s4/tsz2759/networks_project/oboe/Graphs/"
DATA_FILE_PATH = "/home/stu15/s4/tsz2759/networks_project/oboe/Statistics/"

LIVE = "live" 
RECORDED = "recorded"

def main():
    res = getResolutionStream()
    buf = getBufferStream()
    
    res_copy = copy.deepcopy(res)
    buf_copy = copy.deepcopy(buf)
    
    resolutionChanges = calculateResolutionChanges(res)
    
    resolutionChanges_copy = copy.deepcopy(resolutionChanges)
    
    plotResolutionQuality(res)
    plotFrameBuffering(buf) 
    plotResolutionChanges(resolutionChanges)

    overallQoE = calculateUserQoE(res_copy, buf_copy, resolutionChanges_copy)
    
    plotOverallQoE(overallQoE)

    
def getResolutionStream():
    filepath = DATA_FILE_PATH + "resolution_data.csv"
    res = np.genfromtxt(filepath, delimiter=',');

    return res


def getBufferStream():
    filepath = DATA_FILE_PATH + "buffering_data.csv"
    
    buf = np.genfromtxt(filepath, delimiter=',');
    return buf


def calculateResolutionChanges(resolutionStream):
    resolutionChanges = []
    for i in range(len(resolutionStream)):
        if i == 0:
            resolutionChanges.append(0);
        else:
            resolutionChanges.append(resolutionStream[i-1] - resolutionStream[i])
    
    resolutionChanges = np.abs(resolutionChanges)      
    return resolutionChanges

def calculateUserQoE(resolutionStream, bufferingStream, resolutionChanges):
    streamingQoE = []
    
    for i in range(len(resolutionStream)):
        resolutionStream[i] = (resolutionStream[i] / 32) * 1/3
    
    for i in range(len(bufferingStream)):
        bufferingStream[i] = (1 - bufferingStream[i]) * 1/3
    
    resolutionChanges = resolutionChanges.astype(float)
 
    for i in range(len(resolutionChanges)):
        resolutionChanges[i] = (1 - (float(resolutionChanges[i]) / 32.0)) * 1/3

    for i in range(len(resolutionStream)):
        streamingQoE.append((resolutionStream[i] + bufferingStream[i] + resolutionChanges[i])*100)
    
    return streamingQoE
    

def plotResolutionQuality(resolutionStream):
    fig, ax = plt.subplots()
    
    x = np.linspace(0, STREAMING_SECONDS, STREAMING_SECONDS)
        
    y2 = np.full(STREAMING_SECONDS, 8)
    y3 = np.full(STREAMING_SECONDS, 16)
    y4 = np.full(STREAMING_SECONDS, 32)
            
    ax.plot(x, y4, ':', color=LINE_32_COLOR, label = "32P")
    ax.plot(x, y3, ':', color=LINE_16_COLOR, label = "16P")
    ax.plot(x, y2, ':', color=LINE_8_COLOR, label = "8P")
    
    ax.plot(x, resolutionStream, color=LINE_COLOR)
                
    ax.set_xlim(0,STREAMING_SECONDS)
    ax.set_ylim(0,33)
    
    if IS_LIVE:                
        ax.set_title("Resolution Quality when Streaming Live Media with Oboe")
    else:
        ax.set_title("Resolution Quality when Streaming Recorded Media with Oboe")

    ax.set_xlabel('Media Streaming (Seconds)')
    ax.set_ylabel('Resolution (Pixels x Pixels)')
    ax.legend(loc='lower right', fontsize='small')
    
    if IS_LIVE:
        fig.savefig(BASE_FILE_PATH + 'oboe_streaming_resolution_' + LIVE + '.png')
    else:
        fig.savefig(BASE_FILE_PATH + 'oboe_streaming_resolution_' + RECORDED + '.png')
    
    
def plotFrameBuffering(bufferingStream):
    fig, ax = plt.subplots()
    
    x = np.linspace(0, STREAMING_SECONDS, STREAMING_SECONDS)
            
    ax.plot(x, bufferingStream, color=LINE_COLOR)
                
    ax.set_xlim(0,STREAMING_SECONDS)
    ax.set_ylim(-0.1, 1.1)
    
    if IS_LIVE:                
        ax.set_title("Frames Buffered when Streaming Live Media with Oboe")
    else:
        ax.set_title("Frames Buffered when Streaming Recorded Media with Oboe")

    ax.set_xlabel('Media Streaming (Seconds)')
    ax.set_ylabel('Frame Buffering')
    
    if IS_LIVE:
        fig.savefig(BASE_FILE_PATH + 'oboe_streaming_buffering_' + LIVE + '.png')
    else:
        fig.savefig(BASE_FILE_PATH + 'oboe_streaming_buffering_' + RECORDED + '.png')


def plotResolutionChanges(resolutionChanges):
    fig, ax = plt.subplots()
    
    x = np.linspace(0, STREAMING_SECONDS, STREAMING_SECONDS)
        
    y2 = np.full(STREAMING_SECONDS, 8)
    y3 = np.full(STREAMING_SECONDS, 16)
    y5 = np.full(STREAMING_SECONDS, 24)
    y4 = np.full(STREAMING_SECONDS, 32)
            
    ax.plot(x, y4, ':', color=LINE_COLOR, label = "32P")
    ax.plot(x, y5, ":", color=LINE_32_COLOR, label = "24P")
    ax.plot(x, y3, ':', color=LINE_16_COLOR, label = "16P")
    ax.plot(x, y2, ':', color=LINE_8_COLOR, label = "8P")
    
    ax.plot(x, resolutionChanges, color=LINE_COLOR)
                
    ax.set_xlim(0, STREAMING_SECONDS)
    ax.set_ylim(0, 33)
    
    if IS_LIVE:                
        ax.set_title("Bitrate Changes when Streaming Live Media with Oboe")
    else:
        ax.set_title("Bitrate Changes when Streaming Recorded Media with Oboe")

    ax.set_xlabel('Media Streaming (Seconds)')
    ax.set_ylabel('Resolution Changes (Pixel Change)')
    ax.legend(loc='upper right', fontsize='small')
    
    if IS_LIVE:
        fig.savefig(BASE_FILE_PATH + 'oboe_resolution_changes_' + LIVE + '.png')
    else:
        fig.savefig(BASE_FILE_PATH + 'oboe_resolution_changes_' + RECORDED + '.png')
 
    
def plotOverallQoE(overallQoE):   
    fig, ax = plt.subplots()
    
    x = np.linspace(0, STREAMING_SECONDS, STREAMING_SECONDS)
        
    y2 = np.full(STREAMING_SECONDS, 60)
    y3 = np.full(STREAMING_SECONDS, 80)
    y4 = np.full(STREAMING_SECONDS, 100)
            
    ax.plot(x, y4, ':', color=LINE_32_COLOR, label = "Best")
    ax.plot(x, y3, ':', color=LINE_16_COLOR, label = "Better")
    ax.plot(x, y2, ':', color=LINE_8_COLOR, label = "Good")
    
    ax.plot(x, overallQoE, color=LINE_COLOR)
                
    ax.set_xlim(0, STREAMING_SECONDS)
    ax.set_ylim(0, 105)
    
    if IS_LIVE:                
        ax.set_title("Overall QoE when Streaming Live Media with Oboe")
    else:
        ax.set_title("Overall QoE when Streaming Recorded Media with Oboe")

    ax.set_xlabel('Media Streaming (Seconds)')
    ax.set_ylabel('Quality of Experience (%)')
    ax.legend(loc='lower left', fontsize='small')
    
    if IS_LIVE:
        fig.savefig(BASE_FILE_PATH + 'oboe_streaming_QoE_' + LIVE + '.png')
    else:
        fig.savefig(BASE_FILE_PATH + 'oboe_streaming_QoE_' + RECORDED + '.png')
    
    
if __name__ == "__main__":
    main()
