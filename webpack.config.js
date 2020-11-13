module.exports = {
    entry: "./scripts/Main.jsx",
    output: {
        path: __dirname,
        filename: "./static/script.js"
    },
    module: {
        rules: [
            { test: /\.css$/, loader: "style-loader!css-loader" },
            {
                test: /\.(js|jsx)$/,
                exclude: /(node_modules)/,
                loader: 'babel-loader',
                options: {
                     presets: [
                        '@babel/preset-react',
                        [
                            '@babel/preset-env',
                            {
                              targets: {
                                esmodules: false
                              }
                            }
                        ]
                    ]
                }
            }
        ]
    },
    resolve: {
    extensions: ['.js', '.jsx'],
  }
};