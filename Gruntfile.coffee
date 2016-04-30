module.exports = (grunt) ->
    grunt.initConfig
        pkg: grunt.file.readJSON 'package.json'
        stylus:
            compile:
                options:
                    compress: false
                files:
                    'tmp/main.css': [
                        'veldthollow/media/styles/main/base.styl',
                        'veldthollow/media/styles/main/**/*.styl'
                    ]
                    'tmp/splash.css': 'veldthollow/media/styles/splash/**/*.styl'
                    'tmp/maintenance.css': 'veldthollow/media/styles/maintenance/**/*.styl'
        #coffee:
        #    compile:
        #        files:
        #            'tmp/main.js': 'scripts/**/*.coffee'
        uglify:
            scripts:
                files:
                    'veldthollow/static/js/main.js': [
                        'scripts/vendor/bootstrap.min.js'
                        #'tmp/main.js'
                    ]
        concat:
            styles:
                files:
                    'veldthollow/static/css/main.css': [
                        'tmp/main.css'
                    ]
                    'veldthollow/static/css/splash.css': [
                        'tmp/splash.css'
                    ]
                    'veldthollow/static/css/maintenance.css': [
                        'tmp/maintenance.css'
                    ]
        watch:
            #coffee:
            #    files: 'scripts/**/*.coffee'
            #    tasks: ['coffee', 'uglify:scripts']
            js:
                files: 'veldthollow/media/scripts/**/*.js'
                tasks: ['uglify:scripts']
            stylus:
                files: 'veldthollow/media/styles/**/*.styl'
                tasks: ['stylus', 'concat:styles']
            css:
                files: 'veldthollow/media/styles/**/*.css'
                tasks: ['concat:styles']

    grunt.loadNpmTasks 'grunt-contrib-uglify'
    grunt.loadNpmTasks 'grunt-contrib-concat'
    #grunt.loadNpmTasks 'grunt-contrib-coffee'
    grunt.loadNpmTasks 'grunt-contrib-stylus'
    grunt.loadNpmTasks 'grunt-contrib-watch'

    grunt.registerTask 'default', ['stylus', 'concat', 'uglify'] #'coffee', 'uglify']
    grunt.registerTask 'w', ['default', 'watch']

