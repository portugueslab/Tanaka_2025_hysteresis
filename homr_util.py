from scipy.stats import wilcoxon, ranksums
from scipy.optimize import curve_fit
import numpy as np
from matplotlib import pyplot as plt
import colorcet as cc
from matplotlib import cm
from matplotlib import colors as cl


def set_rcParams():
    '''
    Set matplotlib rcParams so that the resulting SVG panels can be figure panels without manual resizing
    '''
    plt.rcParams['svg.fonttype'] = 'none' # assume fonts are installed and do not convert text to path in svg
    plt.rcParams['font.family'] = 'Arial'
    plt.rcParams['font.style'] = 'normal'
    plt.rcParams['font.size'] = 6

    plt.rcParams['axes.titlesize'] = 7
    plt.rcParams['axes.labelsize'] = 6
    plt.rcParams['xtick.labelsize'] = 5
    plt.rcParams['ytick.labelsize'] = 5

    plt.rcParams['lines.linewidth'] = 1
    plt.rcParams['savefig.dpi'] = 300
    plt.rcParams["legend.frameon"] = False
    plt.rcParams['patch.linewidth'] = 0


def nancoxon(X):
    '''
    Do wilcoxon test while ignoring NaNs
    '''
    return wilcoxon(X[~np.isnan(X)])

def put_scalebar(ax, x, mag, unit, horizontal=False):
    '''
    Does what it says
    '''
    y = mag
    if not horizontal:
        ax.plot([x,x],[y,y+mag], 'k-', linewidth=1.5)
        ax.text(x+1, y+mag/2, str(mag)+' '+unit)
    else:
        ax.plot([y,y+mag], [x,x], 'k-', linewidth=1.5)
        ax.text(y, x, str(mag)+' '+unit)
        
def plot_mean_sem(ax, x, y, label='', lw=1, *args, **kwargs):
    '''
    Given a 2D data matrix, plot the mean and the standard error around it
    '''
    N = y.shape[0]
    mean_y = np.mean(y, axis=0)
    sem_y = np.nanstd(y, axis=0) / np.sqrt(N)
    ax.plot(x, mean_y, label=label, lw=lw, *args, **kwargs)
    ax.fill_between(x, mean_y-sem_y, mean_y+sem_y, alpha=0.2, zorder=-2, lw=0, *args, **kwargs)

def toggle_spines(ax, top, bottom, right, left):
    '''
    A shorthand for removing plot spines
    '''
    ax.spines.top.set_visible(top)
    ax.spines.bottom.set_visible(bottom)
    ax.spines.right.set_visible(right)
    ax.spines.left.set_visible(left)
    if not bottom:
        ax.set_xticks([])
    if not left:
        ax.set_yticks([])

def jitter_scatter(X, ax):
    '''
    Plot individual data point with jitters on X-axis so they are easier to see
    Used to show individual animal data on bar-plots
    '''
    n_row = X.shape[0]
    n_col = X.shape[1]
    pos_mat = np.tile(np.arange(n_col), (n_row,1)) + (np.random.rand(n_row, n_col)-0.5)/4
    ax.scatter(pos_mat, X, alpha=0.2, color=(.80,0.5,0.25))
    ax.scatter(np.arange(n_col), np.nanmedian(X,axis=0), color=(0.3,0,0.8), marker='*')
        
        
def scatter_bar(data, ax=[], color=cm.viridis, condnames=[], connect=False):
    '''
    Bar plots with individual animal data (with X-jitter)
    Can plot data paired or un-paired
    Return stats also
    '''
    
    # if axis is not explicitly provided, we use gcf
    if not ax:
        ax = plt.gca()
    
    # data can be 2d array (matched) or a list of 1d arrays
    islist = isinstance(data, list) or isinstance(data, tuple)
    isarray = isinstance(data, np.ndarray)
    if islist==isarray:
        print('wrong type')
        return
    
    if isarray and len(data.shape)!=2:
        print('wrong dimensions')
        return

    #  calculate mean and sem
    if islist:
        ncond = len(data)
        means = [np.mean(y) for y in data]
        sems = [np.std(y)/np.sqrt(len(y)) for y in data]
    else:
        ncond = data.shape[0]
        means = np.mean(data, axis=1)
        sems = np.std(data, axis=1) / np.sqrt(data.shape[1])

    # prepare color
    if isinstance(color, cl.Colormap): # colormap provided
        color_list = [color(x) for x in np.linspace(0, 1, ncond, endpoint=True)]
    else: # otherwise assume this is already a list of colors
        color_list = color
    
    x = np.arange(ncond)
    
    # bar plot
    ax.bar(x, means, color=color_list, alpha=0.5, zorder=0)
            
    # errorbars & individual data points
    all_jittered_x = []
    for i in range(ncond):
        y = data[i]
        n_sample = len(y)
        jittered_x = i + (np.random.rand(n_sample)-0.5) * 0.25
        all_jittered_x.append(jittered_x)
        ax.scatter(jittered_x, y, color=color_list[i % len(color_list)], s=5, zorder=2)
        ax.plot((i,i), (means[i]-sems[i], means[i]+sems[i]), 'k-', lw=1.5, zorder=3)
        
    # connecting dots (ignored for lists = unpaired data)
    if connect and isarray:
        all_jittered_x = np.asarray(all_jittered_x)
        for i in range(data.shape[1]):
            ax.plot(all_jittered_x[:, i], data[:, i], color=(0.5,0.5,0.5), alpha=0.5, zorder=1, lw=0.5)
        
    if condnames:
        ax.set_xticks(x)
        ax.set_xticklabels(condnames)
        
    # statistics
    pval = np.zeros((ncond,ncond))
    for i in range(ncond):
            for j in range(ncond):
                if i!=j:
                    if islist:
                        _, pval[i, j] = ranksums(data[i], data[j])
                    else:
                        _, pval[i, j] = wilcoxon(data[i], data[j])
    np.set_printoptions(precision=3)
    return pval
        
# utility function for exponential fitting
def fit_exponential(BTA, kernel_duration, kernel_resolution):
    '''
    Log transform the data, do lienar regression
    '''
    t_vec = np.arange(0, kernel_duration, 1/kernel_resolution)
    regressor = np.vstack((t_vec, np.ones(len(t_vec))))
    BTA = BTA[::-1]
    nonneg = BTA>0
    BTA_nonneg = BTA[nonneg]
    alpha, beta = np.linalg.lstsq(regressor[:, nonneg].T, np.log(BTA_nonneg), rcond=None)[0]
    tau = 1/alpha
    return tau, beta, t_vec

def scaled_exponential(t, alpha, beta):
    return np.exp(alpha*t + beta)

def fit_exponential_direct(BTA, kernel_duration, kernel_resolution, p0=(-1.0, 1.0)):
    '''
    Use nonlinear curve fitting to directly fit exponential
    '''
    t_vec = np.arange(0, kernel_duration, 1/kernel_resolution)
    try:
        popt, _ = curve_fit(scaled_exponential, t_vec, BTA[::-1], bounds=((-np.Inf, -np.Inf), (0, np.Inf)), p0=p0)
    except:
        print('nonlinear fitting did not converge')
        popt = (np.nan, np.nan)
    return 1/popt[0], popt[1], t_vec


def logistic(t, T, tau, y0):
    """
    Logistic decay function
    T represents half-decay point
    """
    return y0 / (1 + np.exp((t-T)/tau))


def fit_logistic(BTA, kernel_duration, kernel_resolution, p0=(1,1,1)):
    '''
    Does what it says
    '''
    # for the sake of consistency, the first element of BTA is furthest in the past
    t_vec = np.arange(0, kernel_duration, 1/kernel_resolution)
    try:
        popt, _ = curve_fit(logistic, t_vec, BTA[::-1], bounds=((0, 0, 0), (np.Inf, np.Inf, np.Inf)), p0=p0)
    except:
        print('nonlinear fitting did not converge')
        popt = (np.nan, np.nan, np.nan)
    return popt[0], popt[1], popt[2], t_vec

def cut_triggered_snip(data, t, triggers, n_sample_pre, n_sample_post):
    '''
    Given time series data, time axis, and a list of time points, cut out
    snippets around the provided time points
    For event triggered analysis of all sorts
    '''
    snips = []
    for this_t in triggers:
        if this_t > max(t):
            continue
        trigger_ind = np.argmax(t > this_t)
        try:
            snips.append(data[:, trigger_ind + np.arange(-n_sample_pre, n_sample_post)])
        except:
            print('too close to the end of experiment')
    return np.dstack(snips)

def draw_reference(ax, x=0, y=0):
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    if not np.isnan(y):
        ax.plot(xlim, (y,y), 'k--', lw=1)
    if not np.isnan(x):
        ax.plot((x,x), ylim, 'k--', lw=1)