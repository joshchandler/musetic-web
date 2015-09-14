var gulp = require('gulp'),
    $ = require('gulp-load-plugins')(),
    path = require('path'),
    del = require('del'),
    runSequence = require('run-sequence'),
    argv = require('minimist')(process.argv.slice(2));

var appRoot = path.resolve(__dirname);
var staticRoot = path.resolve(appRoot, 'static/');
var stylesPath = path.resolve(appRoot, 'styles/');

var RELEASE = !!argv.release;
var AUTOPREFIXER_BROWSERS = [
    'ie >= 10',
    'ie_mob >= 10',
    'ff >= 30',
    'chrome >= 34',
    'safari >= 7',
    'opera >= 23',
    'ios >= 7',
    'android >= 4.4',
    'bb >= 10'
];

var src = {};
var watch = false;

// The default task
gulp.task('default', ['watch']);

// Styles
gulp.task('styles', function () {
    src.styles = stylesPath + '/**/*.{css,scss}';
    return gulp.src(src.styles)
        .pipe($.plumber())
        .pipe($.sass({
            sourceMap: !RELEASE,
            sourceMapBasepath: __dirname
        }))
        .on('error', console.error.bind(console))
        .pipe($.autoprefixer({browsers: AUTOPREFIXER_BROWSERS}))
        .pipe($.csscomb())
        .pipe($.concat('main.css'))
        .pipe($.minifyCss())
        .pipe(gulp.dest(staticRoot + '/musetic/css/'))
        .pipe($.size({title: 'styles'}));
});

gulp.task('build', function (cb) {
    runSequence(['styles'], cb);
});

gulp.task('watch', ['build'], function () {
    runSequence('build', function () {
        gulp.watch(src.styles, ['styles']);
    });
});