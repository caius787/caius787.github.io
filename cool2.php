<?php
// object with date of birth
$bday = new DateTime('15.10.1976');    // day.month.year (or: year-month-day)

// object with another specified date (here: 2012-03-01)
$d2 = new DateTime('2012-03-01 00:00:00');

// object with the difference between $d2 and $bday (y = year, m = month, d = day)
$diff2 = $d2->diff($bday);

// output
echo '<br>'. $diff2->y .' years, '. $diff2->m .' month, '. $diff2->d .' days';
// 35 years, 4 month, 15 days
?>
