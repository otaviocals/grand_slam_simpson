


# rematch

> Match Regular Expressions with a Nicer 'API'

[![Linux Build Status](https://travis-ci.org/MangoTheCat/rematch.svg?branch=master)](https://travis-ci.org/MangoTheCat/rematch)
[![Windows Build status](https://ci.appveyor.com/api/projects/status/github/MangoTheCat/rematch?svg=true)](https://ci.appveyor.com/project/gaborcsardi/rematch)
[![](http://www.r-pkg.org/badges/version/rematch)](http://www.r-pkg.org/pkg/rematch)
[![CRAN RStudio mirror downloads](http://cranlogs.r-pkg.org/badges/rematch)](http://www.r-pkg.org/pkg/rematch)
[![Coverage Status](https://img.shields.io/codecov/c/github/MangoTheCat/rematch/master.svg)](https://codecov.io/github/MangoTheCat/rematch?branch=master)

A small wrapper on 'regexpr' to extract the matches and captured groups
from the match of a regular expression to a character vector.

## Installation


```r
source("https://install-github.me/MangoTheCat/rematch")
```

## Usage


```r
library(rematch)
```


```r
dates <- c("2016-04-20", "1977-08-08", "not a date", "2016",
  "76-03-02", "2012-06-30", "2015-01-21 19:58")
isodate <- "([0-9]{4})-([0-1][0-9])-([0-3][0-9])"
re_match(text = dates, pattern = isodate)
```

```
#>      .match                       
#> [1,] "2016-04-20" "2016" "04" "20"
#> [2,] "1977-08-08" "1977" "08" "08"
#> [3,] NA           NA     NA   NA  
#> [4,] NA           NA     NA   NA  
#> [5,] NA           NA     NA   NA  
#> [6,] "2012-06-30" "2012" "06" "30"
#> [7,] "2015-01-21" "2015" "01" "21"
```


```r
isodaten <- "(?<year>[0-9]{4})-(?<month>[0-1][0-9])-(?<day>[0-3][0-9])"
re_match(text = dates, pattern = isodaten)
```

```
#>      .match       year   month day 
#> [1,] "2016-04-20" "2016" "04"  "20"
#> [2,] "1977-08-08" "1977" "08"  "08"
#> [3,] NA           NA     NA    NA  
#> [4,] NA           NA     NA    NA  
#> [5,] NA           NA     NA    NA  
#> [6,] "2012-06-30" "2012" "06"  "30"
#> [7,] "2015-01-21" "2015" "01"  "21"
```

## License

MIT © Mango Solutions
