import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeRaw from "rehype-raw";
import { Box, Typography } from "@mui/material";

export default function ChatMarkdown({ content }) {
  return (
    <Box
      sx={{
        "& ul": { paddingLeft: 3, marginTop: 1 },
        "& li": { marginBottom: 1 },
        "& p": { margin: 0 },
        "& strong": { fontWeight: 700 },
      }}
    >
      <ReactMarkdown
        children={content}
        remarkPlugins={[remarkGfm]}
        rehypePlugins={[rehypeRaw]}
        components={{
          p: ({ children }) => (
            <Typography variant="body2" sx={{ mb: 1 }}>
              {children}
            </Typography>
          ),
          li: ({ children }) => (
            <li>
              <Typography variant="body2">{children}</Typography>
            </li>
          ),
        }}
      />
    </Box>
  );
}
