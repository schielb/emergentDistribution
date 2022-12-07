import pa_test
import se_test
import matplotlib.pyplot as plt 

standard_deviations_se_rr = []
standard_deviations_pa_rr = []

standard_deviations_se_rs = []
standard_deviations_pa_rs = []

standard_deviations_se_es = []
standard_deviations_pa_es = []

percent_collisions_se_rr = []
percent_collisions_pa_rr = []

percent_collisions_se_rs = []
percent_collisions_pa_rs = []

percent_collisions_se_es = []
percent_collisions_pa_es = []

centers_se_rr = []
centers_pa_rr = []

centers_se_rs = []
centers_pa_rs = []

centers_se_es = []
centers_pa_es = []

for i in range(len(pa_test.Rand_rand)):
  standard_deviations_se_rr.append(se_test.Rand_rand[i][0])
  standard_deviations_pa_rr.append(pa_test.Rand_rand[i][0])
  standard_deviations_se_rs.append(se_test.Rand_loop[i][0])
  standard_deviations_pa_rs.append(pa_test.Rand_loop[i][0])
  standard_deviations_se_es.append(se_test.Emerge_step[i][0])
  standard_deviations_pa_es.append(pa_test.Emerge_step[i][0])
  percent_collisions_se_rr.append(se_test.Rand_rand[i][1])
  percent_collisions_pa_rr.append(pa_test.Rand_rand[i][1])
  percent_collisions_se_rs.append(se_test.Rand_loop[i][1])
  percent_collisions_pa_rs.append(pa_test.Rand_loop[i][1])
  percent_collisions_se_es.append(se_test.Emerge_step[i][1])
  percent_collisions_pa_es.append(pa_test.Emerge_step[i][1])
  centers_se_rr.append(se_test.Rand_rand[i][2])
  centers_pa_rr.append(pa_test.Rand_rand[i][2])
  centers_se_rs.append(se_test.Rand_loop[i][2])
  centers_pa_rs.append(pa_test.Rand_loop[i][2])
  centers_se_es.append(se_test.Emerge_step[i][2])
  centers_pa_es.append(pa_test.Emerge_step[i][2])

plotting = [
  [ "Comparison: Random-Random - Standard Deviation",
    [standard_deviations_se_rr, "SE - Rand-rand - StanDev", "Iterations", "Standard Deviation", "The standard deviation from the set of totals of each sensor type."],
    [standard_deviations_pa_rr, "PA - Rand-rand - StanDev", "Iterations", "Standard Deviation", "The standard deviation from the set of totals of each sensor type."]
  ],
  [ "Comparison: Random-Loop - Standard Deviation",
    [standard_deviations_se_rs, "SE - Rand-loop - StanDev", "Iterations", "Standard Deviation", "The standard deviation from the set of totals of each sensor type."],
    [standard_deviations_pa_rs, "PA - Rand-loop - StanDev", "Iterations", "Standard Deviation", "The standard deviation from the set of totals of each sensor type."]
  ],
  [ "Comparison: Emerge Step - Standard Deviation",
    [standard_deviations_se_es, "SE - Emerge-step - StanDev", "Iterations", "Standard Deviation", "The standard deviation from the set of totals of each sensor type."],
    [standard_deviations_pa_es, "PA - Emerge-step - StanDev", "Iterations", "Standard Deviation", "The standard deviation from the set of totals of each sensor type."]
  ],
  [ "Comparison: Random-Random - Percent Collisions",
    [percent_collisions_se_rr, "SE - Rand-rand - PercCol", "Iterations", "Percent Collisions", "The percent of neighbors whose type matches center node"],
    [percent_collisions_pa_rr, "PA - Rand-rand - PercCol", "Iterations", "Percent Collisions", "The percent of neighbors whose type matches center node"]
  ],
  [ "Comparison: Random-Loop - Percent Collisions",
    [percent_collisions_se_rs, "SE - Rand-loop - PercCol", "Iterations", "Percent Collisions", "The percent of neighbors whose type matches center node"],
    [percent_collisions_pa_rs, "PA - Rand-loop - PercCol", "Iterations", "Percent Collisions", "The percent of neighbors whose type matches center node"]
  ],
  [ "Comparison: Emerge Step - Percent Collisions",
    [percent_collisions_se_es, "SE - Emerge-step - PercCol", "Iterations", "Percent Collisions", "The percent of neighbors whose type matches center node"],
    [percent_collisions_pa_es, "PA - Emerge-step - PercCol", "Iterations", "Percent Collisions", "The percent of neighbors whose type matches center node"]
  ],
  [ "Comparison: Random-Random - Center of Each Color",
    [centers_se_rr, "SE - Rand-rand - CentDist", "Iterations", "CentDist", "The distance from the center that the average of each color is."],
    [centers_pa_rr, "PA - Rand-rand - CentDist", "Iterations", "CentDist", "The distance from the center that the average of each color is."]
  ],
  [ "Comparison: Random-Loop - Center of Each Color",
    [centers_se_rs, "SE - Rand-loop - CentDist", "Iterations", "CentDist", "The distance from the center that the average of each color is."],
    [centers_pa_rs, "PA - Rand-loop - CentDist", "Iterations", "CentDist", "The distance from the center that the average of each color is."]
  ],
  [ "Comparison: Emerge Step - Center of Each Color",
    [centers_se_es, "SE - Emerge-step - CentDist", "Iterations", "CentDist", "The distance from the center that the average of each color is."],
    [centers_pa_es, "PA - Emerge-step - CentDist", "Iterations", "CentDist", "The distance from the center that the average of each color is."]
  ]
]

# for plot_set in plotting:
#   # fig = plt.figure()
#   # ax = fig.add_subplot()
#   plt.figure(plot_set[0])

#   plt.subplot(1,2,1)
#   plt.plot(plot_set[1][0])
#   plt.title(plot_set[1][1])
#   plt.xlabel(plot_set[1][2])
#   plt.ylabel(plot_set[1][3])
#   # #plt.figtext(plot_set[0][4])
#   # ax.text(3, 8, plot_set[0][4], style='italic',
#   #       bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})

#   plt.subplot(1,2,2)
#   plt.plot(plot_set[2][0])
#   plt.title(plot_set[2][1])
#   plt.xlabel(plot_set[2][2])
#   plt.ylabel(plot_set[2][3])
#   # #plt.figtext(plot_set[1][4])
#   # ax.text(3, 8, plot_set[1][4], style='italic',
#   #       bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})

#   # show plot
#   plt.show()

for i in range(3):
  # fig = plt.figure()
  # ax = fig.add_subplot()
  plt.figure(plotting[i*3][0], figsize=(17, 19))

  plt.subplot(3,2,1)
  plt.plot(plotting[i*3][1][0])
  plt.title(plotting[i*3][1][1])
  plt.xlabel(plotting[i*3][1][2])
  plt.ylabel(plotting[i*3][1][3])
  # #plt.figtext(plot_set[0][4])
  # ax.text(3, 8, plot_set[0][4], style='italic',
  #       bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})

  plt.subplot(3,2,2)
  plt.plot(plotting[i*3][2][0])
  plt.title(plotting[i*3][2][1])
  plt.xlabel(plotting[i*3][2][2])
  plt.ylabel(plotting[i*3][2][3])
  # #plt.figtext(plot_set[1][4])
  # ax.text(3, 8, plot_set[1][4], style='italic',
  #       bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})

  plt.subplot(3,2,3)
  plt.plot(plotting[i*3+1][1][0])
  plt.title(plotting[i*3+1][1][1])
  plt.xlabel(plotting[i*3+1][1][2])
  plt.ylabel(plotting[i*3+1][1][3])
  # #plt.figtext(plot_set[0][4])
  # ax.text(3, 8, plot_set[0][4], style='italic',
  #       bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})

  plt.subplot(3,2,4)
  plt.plot(plotting[i*3+1][2][0])
  plt.title(plotting[i*3+1][2][1])
  plt.xlabel(plotting[i*3+1][2][2])
  plt.ylabel(plotting[i*3+1][2][3])
  # #plt.figtext(plot_set[1][4])
  # ax.text(3, 8, plot_set[1][4], style='italic',
  #       bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})

  plt.subplot(3,2,5)
  plt.plot(plotting[i*3+2][1][0])
  plt.title(plotting[i*3+2][1][1])
  plt.xlabel(plotting[i*3+2][1][2])
  plt.ylabel(plotting[i*3+2][1][3])
  # #plt.figtext(plot_set[0][4])
  # ax.text(3, 8, plot_set[0][4], style='italic',
  #       bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})

  plt.subplot(3,2,6)
  plt.plot(plotting[i*3+2][2][0])
  plt.title(plotting[i*3+2][2][1])
  plt.xlabel(plotting[i*3+2][2][2])
  plt.ylabel(plotting[i*3+2][2][3])
  # #plt.figtext(plot_set[1][4])
  # ax.text(3, 8, plot_set[1][4], style='italic',
  #       bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})

  # show plot
  plt.subplots_adjust(left=0.1,
                    bottom=0.1,
                    right=0.9,
                    top=0.9,
                    wspace=0.5,
                    hspace=0.5)
  
  plt.show()

plt.figure("Speedups")  

plt.subplot(1,3,1)
plt.bar(["Ser", "Par"], [se_test.time_rand, pa_test.time_rand])
# Title to the plot
plt.title("Time: Random-Random")
plt.ylabel("Microseconds")
plt.legend(["Speedup: %.4f" % (se_test.time_rand / pa_test.time_rand)])
# Adding the legends

plt.subplot(1,3,2)
plt.bar(["Ser", "Par"], [se_test.time_loop, pa_test.time_loop])
# Title to the plot
plt.title("Time: Random-Loop")
plt.ylabel("Microseconds")
plt.legend(["Speedup: %.4f" % (se_test.time_loop / pa_test.time_loop)])
# Adding the legends

plt.subplot(1,3,3)
plt.bar(["Ser", "Par"], [se_test.time_emerge, pa_test.time_emerge])
# Title to the plot
plt.title("Time: Emerge Step")
plt.ylabel("Microseconds")
plt.legend(["Speedup: %.4f" % (se_test.time_emerge / pa_test.time_emerge)])
# Adding the legends


plt.show()
  