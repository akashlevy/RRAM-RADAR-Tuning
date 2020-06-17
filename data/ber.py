import matplotlib as mpl, numpy as np, pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

# LaTEX quality figures 
mpl.rcParams.update(
    {
    'text.usetex': True,
    'pgf.texsystem': 'lualatex',
    'pgf.rcfonts': True
    }
)
plt.rc('font', family='serif', serif='Times', size=13)

# Setup figure
fig, ax = plt.subplots(figsize=(4,3))
plt.title('Pulses Required for Target Error')
plt.xlabel('Mean Pulses Required')
plt.ylabel('Error (\%)')
plt.tight_layout()

# Load SDR data
names = ['addr', 'nreads', 'nsets', 'nresets', 'rf', 'if', 'rlo', 'rhi', 'success', 'attempts1', 'attempts2']
fnames = ['ispp/data/ispp-4wl-eval-chip1-6-6-20.csv', 'fppv/data/fppv-4wl-eval-chip1-6-6-20.csv', 'fppv/data/fppv-4wl-eval-chip1-6-6-20.csv', 'sdr/data/infopt/sdr-infopt-4wl-eval-chip1-6-8-20.csv']
fnames = ['ispp/data/ispp-1wl-eval-chip2-6-11-20.csv', 'fppv/data/fppv-1wl-eval-chip2-6-11-20.csv', 'fppv/data/fppv-1wl-eval-chip2-6-11-20.csv', 'sdr/data/infopt/sdr-infopt-1wl-eval-chip2-6-11-20.csv']
for i, fname in enumerate(fnames):
    data = pd.read_csv(fname, delimiter='\t', names=names, index_col=False)
    data['npulses'] = data['nsets'] + data['nresets'] - 1
    rlos = data['rlo'].unique()
    data['bin'] = data['rlo'].apply(lambda x: np.where(rlos == x)[0][0])
    data = data[data['bin'] != 7]
    if i == 1:
        badaddrs = [4103, 4115, 4170, 4242, 4243, 4295, 4437, 4441, 4490, 4532, 4554, 4593, 4607, 4660, 4665, 4670, 4688, 4749, 4854, 4855, 4866, 4896, 4901, 4908, 4935, 4937, 4947, 4962, 4982, 4984, 4986, 4989, 5059, 5120, 5121, 5125, 5126, 5133, 5138, 5150, 5188, 5191, 5221, 5224, 5238, 5246, 5261, 5322, 5330, 5332, 5339, 5344, 5369, 5389, 5390, 5421, 5422, 5437, 5444, 5468, 5481, 5483, 5487, 5490, 5517, 5533, 5549, 5555, 5589, 5603, 5624, 5652, 5687, 5692, 5736, 5760, 5784, 5854, 5872, 5880, 5896, 5901, 5905, 5926, 5927, 5960, 5981, 5987, 6000, 6016, 6019, 6031, 6050, 6075, 6091, 6109, 6129, 6132, 6236, 6245, 6281, 6289, 6306, 6337, 6339, 6355, 6358, 6384, 6425, 6426, 6461, 6468, 6477, 6479, 6500, 6503, 6504, 6508, 6510, 6537, 6542, 6547, 6563, 6591, 6594, 6633, 6664, 6666, 6687, 6706, 6746, 6793, 6805, 6806, 6828, 6831, 6837, 6884, 6898, 6910, 6917, 6927, 6956, 6968, 6986, 6998, 7017, 7033, 7050, 7053, 7055, 7059, 7068, 7073, 7093, 7112, 7114, 7119, 7123, 7128, 7146, 7179, 7183, 7186, 7223, 7236, 7245, 7251, 7263, 7293, 7297, 7300, 7309, 7310, 7312, 7315, 7320, 7327, 7341, 7354, 7357, 7367, 7373, 7376, 7397, 7411, 7428, 7433, 7461, 7469, 7471, 7491, 7498, 7519, 7526, 7545, 7586, 7590, 7606, 7616, 7627, 7676, 7686, 7693, 7714, 7725, 7732, 7733, 7772, 7779, 7786, 7790, 7793, 7814, 7815, 7817, 7823, 7830, 7832, 7858, 7861, 7883, 7916, 7926, 7938, 7954, 7955, 7958, 7963, 7965, 7974, 8013, 8020, 8022, 8032, 8044, 8067, 8070, 8072, 8078, 8086, 8114, 8116, 8119, 8128, 8144, 8149, 8156, 8157, 8160, 8166, 8168, 8173, 8174, 8175, 8237, 8285, 8288, 8289, 8291, 8304, 8317, 8342, 8345, 8361, 8369, 8371, 8373, 8387, 8400, 8409, 8410, 8414, 8418, 8423, 8426, 8430, 8431, 8459, 8462, 8474, 8495, 8504, 8522, 8525, 8530, 8571, 8574, 8585, 8589, 8600, 8616, 8619, 8620, 8625, 8642, 8643, 8655, 8663, 8689, 8694, 8697, 8715, 8728, 8731, 8757, 8766, 8769, 8776, 8782, 8785, 8792, 8800, 8802, 8810, 8815, 8819, 8821, 8837, 8841, 8844, 8851, 8874, 8899, 8911, 8919, 8934, 8937, 8940, 8961, 8969, 8975, 8988, 9006, 9011, 9012, 9014, 9022, 9029, 9047, 9050, 9063, 9069, 9080, 9091, 9095, 9104, 9122, 9138, 9139, 9147, 9152, 9165, 9173, 9183, 9192, 9214, 9221, 9227, 9231, 9237, 9240, 9256, 9260, 9261, 9264, 9265, 9268, 9273, 9287, 9293, 9304, 9307, 9320, 9331, 9335, 9339, 9385, 9389, 9406, 9408, 9413, 9414, 9420, 9424, 9430, 9431, 9432, 9435, 9440, 9445, 9448, 9456, 9469, 9478, 9480, 9485, 9488, 9508, 9509, 9532, 9559, 9567, 9572, 9576, 9579, 9584, 9594, 9602, 9607, 9611, 9615, 9619, 9652, 9673, 9674, 9680, 9696, 9699, 9703, 9709, 9711, 9721, 9728, 9732, 9743, 9747, 9748, 9759, 9764, 9765, 9766, 9769, 9770, 9776, 9793, 9808, 9813, 9824, 9827, 9842, 9843, 9848, 9852, 9862, 9870, 9896, 9898, 9903, 9909, 9911, 9918, 9924, 9928, 9935, 9936, 9960, 9962, 9965, 9967, 9973, 9986, 9999, 10006, 10007, 10011, 10014, 10015, 10016, 10026, 10029, 10031, 10032, 10038, 10056, 10060, 10067, 10073, 10083, 10085, 10096, 10101, 10106, 10113, 10119, 10126, 10131, 10142, 10144, 10145, 10166, 10177, 10180, 10186, 10192, 10197, 10199, 10204, 10207, 10212, 10217, 10221, 10223, 10229, 10230, 10231, 10237, 10241, 10244, 10252, 10253, 10264, 10272, 10274, 10285, 10286, 10291, 10294, 10300, 10309, 10314, 10316, 10317, 10320, 10324, 10333, 10335, 10344, 10345, 10348, 10350, 10355, 10357, 10359, 10362, 10369, 10374, 10376, 10377, 10379, 10380, 10382, 10392, 10407, 10422, 10424, 10429, 10430, 10431, 10447, 10452, 10463, 10467, 10473, 10485, 10486, 10487, 10501, 10520, 10526, 10531, 10547, 10560, 10572, 10581, 10583, 10619, 10622, 10628, 10634, 10657, 10669, 10676, 10737, 10760, 10762, 10766, 10774, 10783, 10790, 10792, 10795, 10802, 10805, 10818, 10826, 10832, 10859, 10866, 10877, 10890, 10892, 10902, 10908, 10912, 10925, 10928, 10931, 10940, 10948, 10960, 10978, 10984, 10985, 11003, 11005, 11006, 11011, 11027, 11036, 11042, 11050, 11058, 11067, 11068, 11072, 11079, 11092, 11099, 11110, 11111, 11118, 11125, 11126, 11129, 11142, 11150, 11166, 11174, 11178, 11185, 11201, 11215, 11233, 11236, 11276, 11284, 11286, 11295, 11299, 11301, 11317, 11346, 11356, 11363, 11371, 11373, 11374, 11376, 11380, 11395, 11405, 11406, 11427, 11443, 11449, 11460, 11473, 11476, 11490, 11491, 11495, 11512, 11527, 11532, 11536, 11540, 11541, 11561, 11573, 11582, 11584, 11589, 11593, 11597, 11619, 11644, 11645, 11648, 11668, 11695, 11696, 11702, 11708, 11715, 11720, 11723, 11742, 11745, 11746, 11754, 11768, 11782, 11785, 11786, 11792, 11798, 11800, 11825, 11827, 11881, 11909, 11919, 11921, 11926, 11939, 11942, 11946, 11949, 11952, 11965, 11972, 11974, 11996, 12010, 12013, 12026, 12043, 12045, 12052, 12055, 12057, 12064, 12075, 12077, 12086, 12087, 12102, 12115, 12123, 12126, 12130, 12151, 12152, 12159, 12162, 12180, 12183, 12198, 12200, 12206, 12210, 12211, 12219, 12221, 12223, 12226, 12227, 12244, 12248, 12253, 12256, 12260, 12262, 12263, 12266, 12272, 12278, 12281, 12287, 4137, 4305, 4407, 4423, 4485, 4503, 4630, 4763, 4774, 4785, 4907, 4974, 5006, 5010, 5027, 5075, 5094, 5129, 5172, 5176, 5267, 5304, 5356, 5366, 5385, 5415, 5439, 5494, 5558, 5644, 5683, 5686, 5716, 5733, 5768, 5803, 5840, 6025, 6030, 6055, 6101, 6231, 6328, 6374, 6466, 6482, 6502, 6644, 6658, 6679, 6836, 6933, 7140, 7224, 7269, 7336, 7344, 7380, 7429, 7486, 7512, 7533, 7579, 7639, 7675, 7843, 7880, 7895, 7939, 8050, 8075, 8126, 8234, 8243, 8295, 8313, 8339, 8367, 8383, 8402, 8432, 8437, 8533, 8536, 8549, 8583, 8588, 8613, 8628, 8639, 8672, 8676, 8678, 8691, 8722, 8726, 8759, 8808, 8828, 8836, 8868, 8901, 8932, 8953, 8981, 9032, 9061, 9078, 9126, 9168, 9229, 9302, 9309, 9325, 9340, 9348, 9353, 9355, 9360, 9367, 9402, 9403, 9410, 9447, 9506, 9529, 9531, 9554, 9570, 9601, 9612, 9623, 9678, 9693, 9731, 9783, 9825, 9851, 9874, 9885, 9892,]
        print "Bad addrs:", len(badaddrs)
        data = data[~data['addr'].isin(badaddrs)]

    pulses = []
    bers = []
    for maxpulses in range(200, 0, -1):
        data['success'] = data['success'].astype(bool) & (data['npulses'] <= maxpulses)
        data['npulses'] = data['npulses'].clip(upper=maxpulses)
        pulses.append(data['npulses'].mean())
        bers.append(1-data['success'].mean())
        # if maxpulses == 200:
        #     pulses.append(15)
        #     bers.append(1-data['success'].mean())
    bers = np.array(bers)*100
    if i != 1:
        plt.semilogy(pulses, bers)
    else:
        plt.semilogy(pulses, bers, '--')

    argerr = np.argmin(np.abs(bers - 1))
    print fname
    print pulses[argerr], bers[argerr]
    print pulses[argerr-1], bers[argerr-1]
    plt.annotate('%.2f' % pulses[argerr-1], xy=(pulses[argerr-1], bers[argerr-1]), xytext=(pulses[argerr-1]+0.9, 2), arrowprops=dict(facecolor='black', shrink=0.1, width=1, headwidth=3, headlength=5), fontsize=11, horizontalalignment='center', verticalalignment='center')

plt.semilogy([0, 15], [1, 1], ':')
plt.legend(['ISPP', 'FPPV (-11\% cells)', 'FPPV (orig)', 'SDCFC'], ncol=1, columnspacing=1, handletextpad=0.5, borderpad=0.2, prop={'size': 10})
plt.xlim(2, 15)
plt.ylim(0.6, 100)
ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
ax.yaxis.set_major_formatter(FormatStrFormatter('%d'))
plt.tight_layout()
plt.show()
