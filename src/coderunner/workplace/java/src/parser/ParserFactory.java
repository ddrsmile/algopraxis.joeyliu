package parser;
import java.util.Map;
import java.util.HashMap;
import java.lang.reflect.Constructor;

public class ParserFactory {
    private Map<String, Class<?>> classMap;

    public ParserFactory() {
        classMap = new HashMap<>();
        classMap.put("integer", IntegerParser.class);
        classMap.put("double", DoubleParser.class);
        classMap.put("string", StringParser.class);
    }

    @SuppressWarnings("unchecked")
    public <E> E create(String className) {
        E parser;
        Class<?> clazz = classMap.get(className);

        try {
            Constructor<?> ctor = clazz.getConstructor();
            parser = (E) ctor.newInstance();
        } catch (Throwable e) {
            System.err.println(e);
            parser = null;
        }
        return parser;
    }
}