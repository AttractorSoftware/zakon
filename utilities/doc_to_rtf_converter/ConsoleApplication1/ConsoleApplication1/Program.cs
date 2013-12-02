using Microsoft.Office.Interop.Word;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Word = Microsoft.Office.Interop.Word;
using System.IO;
namespace ConsoleApplication1
{
    class Program
    {
        static void Main(string[] args)
        {
            int count = 1;
            int countOfFailedDocuments = 0;
            int countOfSuccessedDouments = 1;
            string[] files = System.IO.Directory.GetFiles(@".\input", "*.doc");
            foreach(string file in files)
            {
                try
                {
                    var word = new Word.Application();
                    Console.Write(count);
                    Document document = word.Documents.Open(Path.GetFullPath(file));
                    PrintFileName(file);
                    word.Visible = false;
                    document.SaveAs2(Environment.CurrentDirectory + @".\output\" + Path.GetFileNameWithoutExtension(file) + ".rtf", 6);
                    word.Visible = false;
                    document.Close();
                    PrintSuccess();
                    countOfSuccessedDouments++;
                    word.Quit();
                }
                catch (Exception e)
                {
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.Write("Fail\n");
                    Console.ResetColor();
                    throw e;
                    countOfFailedDocuments++;
                }
                finally
                {
                    count++;
                }
            }
            PrintStatisticsAndWait(count, countOfFailedDocuments, countOfSuccessedDouments);
        }

        private static void PrintFileName(string file)
        {
            Console.WriteLine(". " + Path.GetFileNameWithoutExtension(file));
        }

        private static void PrintStatisticsAndWait(int count, int countOfFailedDocuments, int countOfSuccessedDouments)
        {
            Console.WriteLine("\n-----------\nTotally processed " + (count - 1) + " documents");
            Console.ForegroundColor = ConsoleColor.Green;
            Console.WriteLine("Succesed: " + (countOfSuccessedDouments - 1));
            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine("Failed: " + countOfFailedDocuments);
            Console.ReadKey();
        }

        private static void PrintSuccess()
        {
            Console.ForegroundColor = ConsoleColor.Green;
            Console.Write("OK\n");
            Console.ResetColor();
        }
    }
}
