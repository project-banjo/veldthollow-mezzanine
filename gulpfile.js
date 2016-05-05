var gulp = require('gulp');
var gultil = require('gulp-util');
var nib = require('nib');
var sourcemaps = require('gulp-sourcemaps');
var stylus = require('gulp-stylus');

var paths = {
    styl: ['veldthollow/media/styles/**/*.styl'],
    coffee: ['veldthollow/media/scripts/**/*.coffee'],
    root_styles: [
        'veldthollow/media/styles/main.styl',
        'veldthollow/media/styles/maintenance.styl',
        'veldthollow/media/styles/splash.styl'
    ],
    main_coffee: ['veldthollow/media/scripts/main.coffee'],
    output: 'veldthollow/static/'
};

gulp.task('styles', function(){
    return gulp.src(paths.root_styles)
        .pipe(sourcemaps.init())
            .pipe(stylus({
                'use': [nib()]
            }))
        .pipe(sourcemaps.write('./maps', {sourceRoot: null}))
        .pipe(gulp.dest(paths.output + 'css'));
});

gulp.task('scripts', function(){
    //return gulp.src(paths.main_coffee, {read: false})
        //.pipe(sourcemaps.init())
            //.pipe(browserify({
                //'transform': ['coffee-reactify'],
                //'extensions': ['.coffee', '.cjsx']
            //}))
        //.pipe(sourcemaps.write(paths.output))
        //.pipe(rename('app.js'))
        //.pipe(gulp.dest(paths.output));
});

gulp.task('build', ['scripts', 'styles']);

gulp.task('watch', ['build'], function(cb){
    gulp.watch(paths.styl, ['styles']);
    gulp.watch(paths.coffee, ['scripts']);
});
