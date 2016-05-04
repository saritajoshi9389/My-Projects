package lucene.implementation;  // Package for Lucene project Assignment-4

// Required Java Packages
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.Hashtable;
import java.util.Map;
import org.apache.lucene.analysis.core.SimpleAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.CorruptIndexException;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.DocsEnum;
import org.apache.lucene.index.Fields;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.IndexWriter; // key lucene class for indexing
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.index.MultiFields;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopDocs;
import org.apache.lucene.index.Term;
import org.apache.lucene.index.Terms;
import org.apache.lucene.index.TermsEnum;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.DocIdSetIterator;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.store.Directory; // Storage Abstraction class for the index
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Bits;
import org.apache.lucene.util.BytesRef;
import org.apache.lucene.util.Version;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;


public class LuceneImplementation {
    
   IndexWriter writer;
   Directory  fsDir;
   IndexSearcher indexSearcher;
   QueryParser queryParser;
   Query query;
   static String indexDir = "Index";
   public static final int MAX_SEARCH = 3204; 
   String dataDir = "cacm";

   public static void main(String[] args) throws IOException, ParseException 
   {
        LuceneImplementation implementer;
        implementer = new LuceneImplementation();
        implementer.initializeIndex(indexDir); 
        // Below is the array storing the given queries
        //String[] queries = {"portable operating systems", "code optimization for space efficiency",
        //                       "parallel algorithms", "parallel processor in information retrieval"};
        String[] queries = {"portable operating systems", "code optimization for space efficiency",
                              "parallel algorithms"};
        // Numbering the output file for queries
        int query_num = 1;
        //Below code iterates over given list of queries to fetch top 100 documents
        // per query
       for (String query : queries) 
       {
           System.out.print("Query :->" + query + "\t");
           FileWrite fw = new FileWrite("Query_Qutput"+query_num+".txt");
           ArrayList<String> result = implementer.retrieve(query);
           fw.writeResults(result);
           query_num ++;
       }
       implementer.termFrequencyCalculation();
   }
   
   // Lucene Based Indexing
   // Below is the function that initializes indexing based on lucene
   // Path for index creation is ~filepath/Lucene Implementation/Index
   
    public void initializeIndex (String indexDirPath) throws IOException
   {
      File indexDir = new File(indexDirPath);
      fsDir = FSDirectory.open(indexDir);
      // Below is the use of Simple Lucene Analyzer for Lucene 4.7.2
      SimpleAnalyzer analyzer = new SimpleAnalyzer (Version.LUCENE_47);
      IndexWriterConfig config = new IndexWriterConfig(Version.LUCENE_47, analyzer);
      writer = new IndexWriter(fsDir, config);
      writer.deleteAll();
      createIndex();  // Call to create Index function
      writer.close(); // Closes the index writer
   }
    
    public int createIndex() throws IOException{
      File[] files = new File(dataDir).listFiles();
      for (File f : files)  // For all set of files, ignores if its a directory or hidden or not readable file
         if(!f.isDirectory() && !f.isHidden() && f.exists() && f.canRead())
         {
             writer.addDocument(getDocument(f));
         }
      return writer.numDocs();
   }
    
// Function that calls JAVA jsoup to remove the html tags and retrieve the content
   public String filterContent(InputStream is) throws IOException
   {
       BufferedReader br = new BufferedReader(new InputStreamReader(is));
       StringBuilder rawContents=new StringBuilder();
       String sLine;
       String filterText="";
       Elements htmltags;
       while ((sLine = br.readLine()) != null) 
       {
            rawContents.append(sLine);rawContents.append(" ");
       }
       // jsoup parser for removing the unwanted tags
       org.jsoup.nodes.Document doc = Jsoup.parse(rawContents.toString());
       htmltags = doc.select("pre");
       for (Element item : htmltags)
           filterText = filterText+" "+item.ownText();  
       return filterText;  // Stores content without tags
   } 
// Function that retrieves the content, filename and filepath for a document/file
   private Document getDocument(File file) throws IOException
   {
      Document document = new Document();
      InputStream stream = new FileInputStream(file);
       Field contentField = new TextField("contents", filterContent(stream) , Field.Store.NO);
       Field fileNameField = new StringField("filename", file.getName(),Field.Store.YES);
       Field filePathField = new StringField("filepath", file.getCanonicalPath(), Field.Store.YES);
       // Retrieve the essential information for a file//
      document.add(contentField);
      document.add(fileNameField);
      document.add(filePathField);
      return document;
   }   

   ///////END OF INDEXING///////////////////////////////////////////////////////
   
   //// START RETRIEVING for top 100 Doc Ids for each query in queries array
   private ArrayList<String> retrieve(String searchQuery) throws IOException, ParseException
   {
      initQuerySearch();  // Initializes the simple analyzer
      
      query = queryParser.parse(searchQuery); // Lucene Class for parsing
      TopDocs hits = indexSearcher.search(query, MAX_SEARCH);
      System.out.println(hits.totalHits + "  Unique Hits !!!!  " ); // Displays the total hit for query
      ArrayList<String> output = new ArrayList<String>(MAX_SEARCH); // For 100 Doc Ids
      for(ScoreDoc scoreDoc : hits.scoreDocs) 
      {
        Document doc = indexSearcher.doc(scoreDoc.doc);
        output.add(scoreDoc.doc + "\t\t" + doc.get("filename") + "\t\t" + scoreDoc.score);
      }
      writer.close();    
      return output;
   }
   
   // This function initializes the query search via lucene simple analyzer
   public void initQuerySearch() throws IOException
   {
      Directory indexDirectory =  FSDirectory.open(new File(indexDir));
      IndexReader reader = DirectoryReader.open(indexDirectory);
      indexSearcher = new IndexSearcher(reader);
      SimpleAnalyzer analyzer = new SimpleAnalyzer(Version.LUCENE_47);
      IndexWriterConfig config = new IndexWriterConfig(Version.LUCENE_47, analyzer);
      writer = new IndexWriter(indexDirectory, config);
      queryParser = new QueryParser(Version.LUCENE_47, "contents", new SimpleAnalyzer(Version.LUCENE_47));
   }

   /// END OF RETRIEVING !!!
   
   /// START TERM FREQUENCY CALCULATION
   // Use of a hasttable and a comparator to store the values and keep them in sorted order
   
  public void termFrequencyCalculation() throws IOException
   {
    IndexReader reader = DirectoryReader.open(FSDirectory.open(new File(indexDir)));
    
    Bits liveDocs = MultiFields.getLiveDocs(reader);
    Hashtable entries = new Hashtable(); // Stores the term and frequency pair
    Fields fields = MultiFields.getFields(reader);
    for (String field : fields) {
            TermsEnum termEnum = MultiFields.getTerms(reader, "contents").iterator(null);
            BytesRef bytesRef;
            while ((bytesRef = termEnum.next()) != null)
            {
                if (termEnum.seekExact(bytesRef)) 
                {
                    DocsEnum docsEnum = termEnum.docs(liveDocs, null); //Enumerates for all terms
                    if (docsEnum != null)
                    {
                        int doc;
                        while ((doc = docsEnum.nextDoc()) != DocIdSetIterator.NO_MORE_DOCS)
                        {
                            String word = bytesRef.utf8ToString(); // Unicode to String conversion
                            Term term= new Term("contents", word);
                            long termFreq = reader.totalTermFreq(term);
                            if (!entries.containsKey(word))
                                entries.put(word, termFreq);
                        }
                    }
                }
            }
        }
    
    // Comparator code to sort the values in decreasing frequency//
        FileWrite fw = new FileWrite("Term_Frequency.txt"); // Output File
        ArrayList<Map.Entry<String, Long>> sortedList = new ArrayList(entries.entrySet());
        Collections.sort(sortedList, new Comparator<Map.Entry<String, Long>>(){
        public int compare(Map.Entry<String, Long> o1, Map.Entry<String, Long> o2) {
            return o2.getValue().compareTo(o1.getValue());
        }});
        System.out.println("End Of Program");
        fw.writeTermFrequency(sortedList);

    }
   
   /// END OF TERM FREQUENCY CALCULATION for all unique terms in the CACM corpus
}
// End of Program