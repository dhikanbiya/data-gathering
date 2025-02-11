import replpp.Operators.#>
import replpp.Colors

implicit val colors: Colors = Colors.Default  
@main def exec(cpgFile: String, outFile: String) = {
   importCpg(cpgFile)   
   cpg.method.ast.toJsonPretty #> outFile
}